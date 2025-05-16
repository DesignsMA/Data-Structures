import bisect
import matplotlib.pyplot as plt
class BTreeNode:
    """B-Tree Node implementation following Knuth's definition"""
    def __init__(self, m, is_leaf):
        """
        Initialize B-Tree node.

        Args:
            m: Order of the B-Tree (maximum number of children)
            is_leaf: Boolean indicating if the node is a leaf
        """
        self.keys = []          # List to store keys in the node
        self.m = m              # Order of the B-Tree (max children)
        self.children = []      # List to store child nodes
        self.is_leaf = is_leaf  # Whether this node is a leaf

    def is_full(self):
        """Check if the node has reached maximum capacity (m-1 keys)"""
        return len(self.keys) == self.m - 1

    def traverse(self, indentation_level):
        """
        Traverse the tree and print keys with proper indentation.

        Args:
            indentation_level: Current level of indentation for visualization
        """
        indent = "\t" * indentation_level

        if not self.is_leaf:
            for i in range(len(self.keys)):
                # Recursively traverse child nodes first
                self.children[i].traverse(indentation_level + 1)
                print(indent + str(self.keys[i]))

            # Traverse the rightmost child node
            self.children[-1].traverse(indentation_level + 1)
        else:
            # Print keys for leaf nodes
            for key in self.keys:
                print(indent + str(key))

    def split(self):
        """
        Split the node when it's full.

        Returns:
            tuple: (median_key, new_right_node)
        """
        median_index = (self.m - 1) // 2
        median_key = self.keys[median_index]

        # Create new right node
        new_right_node = BTreeNode(self.m, self.is_leaf)

        # Split keys (keys after median go to new node)
        new_right_node.keys = self.keys[median_index + 1:]
        self.keys = self.keys[:median_index]

        if not self.is_leaf:
            # Split children (children after median go to new node)
            new_right_node.children = self.children[median_index + 1:]
            self.children = self.children[:median_index + 1]

        return median_key, new_right_node

    def insert(self, new_key):
        """
        Insert a new key into the subtree rooted at this node.

        Args:
            new_key: Key to be inserted

        Returns:
            tuple: (median_key, new_right_node) if node was split, None otherwise
        """
        new_child_node = None

        if not self.is_leaf:
            # Find the appropriate child for insertion
            insert_pos = bisect.bisect_left(self.keys, new_key)

            # Recursively insert into the child node
            new_child_node = self.children[insert_pos].insert(new_key)

            if new_child_node is not None:
                # Child was split, we need to incorporate the median key
                if not self.is_full():
                    # Insert median key and new child pointer
                    self.keys.insert(insert_pos, new_child_node[0])
                    self.children.insert(insert_pos + 1, new_child_node[1])
                    new_child_node = None
                else:
                    # Current node is full, need to split after insertion
                    self.keys.insert(insert_pos, new_child_node[0])
                    self.children.insert(insert_pos + 1, new_child_node[1])
                    median_key, new_right_node = self.split()
                    return (median_key, new_right_node)
        else:
            # Insert into leaf node
            insert_pos = bisect.bisect_left(self.keys, new_key)
            self.keys.insert(insert_pos, new_key)

            # Check if leaf needs to be split
            if len(self.keys) == self.m:
                return self.split()

        return new_child_node

    def create_new_root(self, median_key, new_right_node):
        """
        Create a new root when the current root splits.

        Args:
            median_key: The key that will be promoted to the new root
            new_right_node: The new right child node

        Returns:
            BTreeNode: The new root node
        """
        new_root = BTreeNode(self.m, False)
        new_root.keys.append(median_key)
        new_root.children.append(self)  # Original node becomes left child
        new_root.children.append(new_right_node)
        return new_root

class BTree:
    """B-Tree implementation following Knuth's definition"""
    def __init__(self, m):
        """
        Initialize B-Tree.

        Args:
            m: Order of the B-Tree (maximum number of children)
        """
        self.root = BTreeNode(m, True)
        self.m = m  # Order of the B-Tree (max children)
        self.fig = None
        self.ax = None

    def insert(self, key):
        """
        Insert a key into the B-Tree.

        Args:
            key: Key to be inserted
        """
        split_result = self.root.insert(key)

        if split_result is not None:
            # Root was split, create a new root
            median_key, new_right_node = split_result
            self.root = self.root.create_new_root(median_key, new_right_node)

    def draw_tree(self):
        """Dibuja el árbol usando matplotlib."""
        self._setup_plot()
        self._draw_node(self.root, x=0, y=0, dx=1.5)
        plt.title("Árbol Binario de Búsqueda")
        plt.show()

    def update_drawing(self):
        """Actualiza el dibujo del árbol."""
        if self.fig is None or not plt.fignum_exists(self.fig.number):
            self._setup_plot()
        else:
            self.ax.clear()
            self.ax.axis("off")

        self._draw_node(self.root, x=0, y=0, dx=1.5)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def _setup_plot(self):
        """Configura la figura de matplotlib."""
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 1)
        self.ax.axis('off')
        self.fig.show()

    def _draw_node(self, node: BTreeNode, x: float, y: float, dx: float):
        """Dibuja un nodo del B-Tree y sus conexiones con los hijos.

        Args:
            node: Nodo actual a dibujar
            x: Posición horizontal del nodo
            y: Posición vertical del nodo
            dx: Espaciado horizontal entre nodos hijos
        """
        if node is not None:
            # Dibuja el rectángulo del nodo con sus claves
            self.ax.text(x, y, str(node.keys), ha='center', va='center',
                       bbox=dict(facecolor='skyblue', boxstyle='round,pad=0.5'))

            if not node.is_leaf:
                # Calcula las posiciones de los hijos
                num_children = len(node.children)
                total_width = dx * (num_children - 1)
                start_x = x - total_width / 2

                # Dibuja las conexiones a cada hijo
                for i, child in enumerate(node.children):
                    child_x = start_x + i * dx
                    # Dibuja línea de conexión
                    self.ax.plot([x, child_x], [y-0.1, y-0.9], 'k-', lw=1)
                    # Dibuja el hijo recursivamente
                    self._draw_node(child, child_x, y-1, dx/2)

    def close_figure(self):
        """Cierra la figura de matplotlib."""
        if self.fig and plt.fignum_exists(self.fig.number):
            plt.close(self.fig)
            self.fig = None
            self.ax = None


print("Creating B-Tree of order 3 (minimum degree 2)")
btree = BTree(6)
for x in [10, 30, 0, 20, 5, 25, 2, 16, 8, 12, 5, 32, 4, 36, 17, 6, 22, 28, 14, 35, 15]:
    btree.insert(x)
    print(f"Inserting: {x}.")
    btree.update_drawing()
    input()
    
