import matplotlib.pyplot as plt
import os
class Nodo:
    """Nodo de un árbol AVL (con altura y factor de balance)."""
    def __init__(self, value=None, parent=None):
        self.value = value
        self.height = 0      # Altura inicializada en 0 (hoja)
        self.fb = 0          # Factor de balance inicial
        self.left = None     # Subárbol izquierdo
        self.right = None    # Subárbol derecho
        self.parent = parent # Nodo padre

    def _update_height(self):
        """Actualiza la altura del nodo en función de sus hijos."""
        left_height = self.left.height if self.left else -1 # si izquierda existe
        right_height = self.right.height if self.right else -1 # si derecha existe
        self.height = 1 + max(left_height, right_height)

    def _update_balance_factor(self):
        """Calcula el factor de balance (FB = altura derecha - altura izquierda)."""
        left_height = self.left.height if self.left else -1 # verifica existencia
        right_height = self.right.height if self.right else -1
        self.fb = right_height - left_height
    
class AVLTree:
    """Implementación de un árbol binario de búsqueda con visualización."""
    def __init__(self):
        self.root = None
        self.fig = None     # Figura de matplotlib para visualización
        self.ax = None      # Ejes de matplotlib

    def empty(self):
        """Verifica si el árbol está vacío."""
        return self.root is None

    def add(self, value):
        """Añade un nuevo valor al árbol."""
        new_node = None
        if self.empty():
            self.root = Nodo(value)
        else:
            parent = self._find_parent(value)
            new_node = Nodo(value, parent)
            if value <= parent.value:
                parent.left = new_node
            else:
                parent.right = new_node
        
        self._balance_tree(new_node)
        
    def _balance_tree(self, node: Nodo):
        "Balancea el ABB mediante rotaciones."
        # ejecuta tras insertar un nodo
        pivot = None # apunta a pivote
        current = node
        while current is not None: # buscar el nodo pivote
            current._update_height() # actualizar altura y fb
            current._update_balance_factor()
            
            if abs(current.fb) >= 2: # si hay un desbalance
                pivot = current
                break
            current = current.parent # desde el nodo hacia la raiz
            
        # si hay pivote el arbol esta en desbalance y hay que rotar
        if pivot is not None:
            self._rotate(pivot, node)
            
        # si no existe el pivote solo se actualizan los fb de los ancestros del nodo
    
    def _rotate(self, p2: Nodo, new_node: Nodo):
        """Realiza rotaciones simples o dobles para balancear el árbol AVL."""
        # Identificar los nodos clave
        p1 = p2.parent  # Padre del pivote (puede ser None si p2 es la raíz)
        # Determinar p3 (hijo con subárbol más grande)
        p3 = p2.right if p2.fb == 2 else p2.left
        p4 = None
        # Determinar p4 (nieto en ruta de inserción)
        if p3 is not None:
            current = new_node
            while current is not None and current != p3 and current.parent != p3:
                current = current.parent
            if current is not None and current.parent == p3:
                p4 = current
            else:
                p4 = None  # No hay p4 en la ruta de inserción
        # Determinar en qué subárbol se insertó
        # Determinar tipo de rotación
        if (p2.fb == 2 and p3.fb >= 0) or (p2.fb == -2 and p3.fb <= 0):
            self._simple_rotation(p1, p2, p3, new_node)
        else:
            self._double_rotation(p1, p2, p3, p4, new_node)

    def _simple_rotation(self, p1: Nodo, p2: Nodo, p3: Nodo, new_node: Nodo):
        """Realiza una rotación simple (LL o RR)."""
        # Determinar tipo de rotación
        if p2.fb == 2:  # Rotación izquierda (LL)
            # Reconfigurar hijos
            p2.right = p3.left
            if p3.left:
                p3.left.parent = p2
            p3.left = p2
        else:  # Rotación derecha (RR)
            p2.left = p3.right
            if p3.right:
                p3.right.parent = p2
            p3.right = p2
    
        # Actualizar padres
        p3.parent = p2.parent
        p2.parent = p3
    
        # Conectar con el árbol
        if p1 is not None:
            if p1.left == p2:
                p1.left = p3
            else:
                p1.right = p3
        else:
            self.root = p3
    
        # Actualizar alturas y factores de balance
        p2._update_height()
        p2._update_balance_factor()
        p3._update_height()
        p3._update_balance_factor()
    
    def _double_rotation(self, p1: Nodo, p2: Nodo, p3: Nodo, p4: Nodo, new_node: Nodo):
        """Realiza una rotación doble (LR o RL)."""
        # Primera rotación (dependiendo del caso)
        if p2.fb == -2:  # Rotación LR
            # Rotación izquierda en p3
            p2.left = p3.right
            if p3.right:
                p3.right.parent = p2
            p3.right = None
            p4.left = p3
            p3.parent = p4
            
            # Rotación derecha en p2
            p4.right = p2
            p2.left = None
        else:  # Rotación RL
            # Rotación derecha en p3
            p2.right = p3.left
            if p3.left:
                p3.left.parent = p2
            p3.left = None
            p4.right = p3
            p3.parent = p4
            
            # Rotación izquierda en p2
            p4.left = p2
            p2.right = None
    
        # Actualizar padres
        p4.parent = p2.parent
        p2.parent = p4
        p3.parent = p4
    
        # Conectar con el árbol
        if p1 is not None:
            if p1.left == p2:
                p1.left = p4
            else:
                p1.right = p4
        else:
            self.root = p4
    
        # Actualizar alturas y factores de balance
        p2._update_height()
        p2._update_balance_factor()
        p3._update_height()
        p3._update_balance_factor()
        p4._update_height()
        p4._update_balance_factor()
    
    def _update_bf_upwards(self, from_node: Nodo, to_node: Nodo):
        """Actualiza factores de balance desde un nodo hasta otro (exclusivo)."""
        current = from_node
        while current and current != to_node:
            current._update_height()
            current._update_balance_factor()
            current = current.parent

    def _find_parent(self, value):
        """Encuentra el nodo padre adecuado para un nuevo valor."""
        node = self.root
        while True:
            next_node = node.left if value <= node.value else node.right
            if next_node is None:
                return node
            node = next_node

    def delete(self, value):
        """Elimina un valor del árbol de forma recursiva y mantiene el balance AVL."""
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        """Función auxiliar recursiva para eliminar un nodo y balancear el árbol."""
        if node is None:
            return None

        # Búsqueda del nodo a eliminar
        if value < node.value:
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:
            node.right = self._delete_rec(node.right, value)
        else:
            # Encontrado el nodo a eliminar
            if node.left is None:
                return node.right  # Caso: sin hijo izquierdo
            elif node.right is None:
                return node.left   # Caso: sin hijo derecho
            else:
                # Caso: dos hijos
                temp = self._min_value_node(node.right)
                node.value = temp.value
                node.right = self._delete_rec(node.right, temp.value)

        # Actualizar altura y factor de balance del nodo actual
        node._update_height()
        node._update_balance_factor()

        # Balancear el nodo si está desbalanceado
        return self._balance_node(node)

    def _balance_node(self, node):
        """Aplica rotaciones si el nodo está desbalanceado."""
        if node.fb > 1:
            if node.right.fb >= 0:
                # Rotación izquierda (LL)
                return self._left_rotate(node)
            else:
                # Rotación derecha-izquierda (RL)
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)
        elif node.fb < -1:
            if node.left.fb <= 0:
                # Rotación derecha (RR)
                return self._right_rotate(node)
            else:
                # Rotación izquierda-derecha (LR)
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        return node

    def _left_rotate(self, z):
        """Rotación izquierda (LL)."""
        y = z.right
        T2 = y.left

        # Realizar rotación
        y.left = z
        z.right = T2

        # Actualizar padres (si es necesario)
        if T2:
            T2.parent = z
        y.parent = z.parent
        z.parent = y

        # Actualizar alturas
        z._update_height()
        y._update_height()

        return y

    def _right_rotate(self, z):
        """Rotación derecha (RR)."""
        y = z.left
        T3 = y.right

        # Realizar rotación
        y.right = z
        z.left = T3

        # Actualizar padres (si es necesario)
        if T3:
            T3.parent = z
        y.parent = z.parent
        z.parent = y

        # Actualizar alturas
        z._update_height()
        y._update_height()

        return y

    def _min_value_node(self, node):
        """Encuentra el nodo con el valor mínimo en un subárbol (igual que antes)."""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def traverse_in_order(self, node):
        """Recorrido in-order del árbol."""
        if node:
            self.traverse_in_order(node.left)
            print(node.value)
            self.traverse_in_order(node.right)

    def traverse_pre_order(self, node):
        """Recorrido pre-order del árbol."""
        if node:
            print(node.value)
            self.traverse_pre_order(node.left)
            self.traverse_pre_order(node.right)

    def traverse_post_order(self, node):
        """Recorrido post-order del árbol."""
        if node:
            self.traverse_post_order(node.left)
            self.traverse_post_order(node.right)
            print(node.value)

    def search(self, node, value):
        """Busca un valor en el árbol."""
        if node is None:
            return None
        elif node.value == value:
            return node
        elif value <= node.value:
            return self.search(node.left, value)
        else:
            return self.search(node.right, value)

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
        self.fig, self.ax = plt.subplots()
        self.ax.axis("off")
        self.fig.show()

    def _draw_node(self, node, x, y, dx):
        """Función auxiliar para dibujar un nodo y sus hijos."""
        if node is not None:
            self.ax.text(x, y, str(node.value), ha='center', 
                        bbox=dict(facecolor='skyblue', boxstyle='circle'))
            if node.left:
                self.ax.plot([x, x - dx], [y, y - 1], 'k-')
                self._draw_node(node.left, x - dx, y - 1, dx / 2)
            if node.right:
                self.ax.plot([x, x + dx], [y, y - 1], 'k-')
                self._draw_node(node.right, x + dx, y - 1, dx / 2)

    def close_figure(self):
        """Cierra la figura de matplotlib."""
        if self.fig and plt.fignum_exists(self.fig.number):
            plt.close(self.fig)
            self.fig = None
            self.ax = None

def edit_menu(tree):
    """Menú para editar el árbol."""
    while True:
        print("\n--- MENÚ DE EDICIÓN ---")
        print("1. Insertar elemento")
        print("2. Eliminar elemento")
        print("3. Cargar árbol desde archivo")
        print("4. Volver al menú principal")

        option = input("Opción: ")
    
        if option == "1":
            value = int(input("Valor a insertar: "))
            tree.add(value)
            tree.update_drawing()
        elif option == "2":
            value = int(input("Valor a eliminar: "))
            tree.delete(value)
            tree.update_drawing()
        elif option == "3":
            filename = input("Nombre del archivo (ej. arbol.txt): ").strip()
            try:
                with open(filename, 'r') as f:
                    numbers = [int(x) for x in f.read().split(',') if x.strip().isdigit()]
                    tree.root = None
                    for num in numbers:
                        tree.add(num)
                    tree.update_drawing()
            except Exception as e:
                print(f"Error: {e}")
        elif option == "4":
            tree.close_figure()
            break


def traversal_menu(tree: AVLTree):
    """Menú para recorrer el árbol."""
    while True:
        tree.update_drawing()
        print("\n--- MENÚ DE RECORRIDOS ---")
        print("1. In-order")
        print("2. Pre-order")
        print("3. Post-order")
        print("4. Buscar valor")
        print("5. Volver")

        option = input("Opción: ")

        if option == "1":
            tree.traverse_in_order(tree.root)
        elif option == "2":
            tree.traverse_pre_order(tree.root)
        elif option == "3":
            tree.traverse_post_order(tree.root)
        elif option == "4":
            val = int(input("Valor a buscar: "))
            node = tree.search(tree.root, val)
            print(f"Valor {val} {'encontrado' if node else 'no encontrado'}")
        elif option == "5":
            break


def main():
    """Función principal del programa."""
    tree = AVLTree()
    
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Editar árbol")
        print("2. Recorridos")
        print("3. Salir")

        option = input("Opción: ")

        if option == "1":
            edit_menu(tree)
        elif option == "2":
            traversal_menu(tree)
        elif option == "3":
            tree.close_figure()
            print("Saliendo...")
            break


if __name__ == "__main__":
    main()