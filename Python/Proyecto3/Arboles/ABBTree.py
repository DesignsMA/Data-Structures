class NodoBinario:
    """NodoBinario de un árbol binario de búsqueda."""
    def __init__(self, value=None, parent=None):
        self.value = value
        self.left = None    # Subárbol izquierdo
        self.right = None   # Subárbol derecho
        self.parent = parent  # NodoBinario padre


class BinarySearchTree:
    """Implementación de un árbol binario de búsqueda con visualización."""
    def __init__(self):
        self.root = None
        self.fig = None     # Figura de matplotlib para visualización
        self.ax = None      # Ejes de matplotlib

    def empty(self):
        """Verifica si el árbol está vacío."""
        return self.root is None

    def insert(self, value):
        """Añade un nuevo valor al árbol."""
        if self.empty():
            self.root = NodoBinario(value)
        else:
            parent = self._find_parent(value)
            if value <= parent.value:
                parent.left = NodoBinario(value, parent)
            else:
                parent.right = NodoBinario(value, parent)

    def _find_parent(self, value):
        """Encuentra el nodo padre adecuado para un nuevo valor."""
        node = self.root
        while True:
            next_node = node.left if value <= node.value else node.right
            if next_node is None:
                return node
            node = next_node

    def delete(self, value):
        """Elimina un valor del árbol de forma recursiva."""
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        """Función auxiliar recursiva para eliminar un nodo."""
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:
            node.right = self._delete_rec(node.right, value)
        else:
            # NodoBinario con un solo hijo o sin hijos
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # NodoBinario con dos hijos: obtener el sucesor inorden (mínimo en subárbol derecho)
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_rec(node.right, temp.value)
        
        return node

    def _min_value_node(self, node):
        """Encuentra el nodo con el valor mínimo en un subárbol."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def traverse_in_order(self, node):
        """Recorrido in-order que retorna una cadena."""
        result = []
        self._traverse_in_order_helper(node, result)
        return " ".join(result)
    
    def _traverse_in_order_helper(self, node, result):
        if node:
            self._traverse_in_order_helper(node.left, result)
            result.append(str(node.value))
            self._traverse_in_order_helper(node.right, result)
    
    def traverse_pre_order(self, node):
        """Recorrido pre-order que retorna una cadena."""
        result = []
        self._traverse_pre_order_helper(node, result)
        return " ".join(result)
    
    def _traverse_pre_order_helper(self, node, result):
        if node:
            result.append(str(node.value))
            self._traverse_pre_order_helper(node.left, result)
            self._traverse_pre_order_helper(node.right, result)
    
    def traverse_post_order(self, node):
        """Recorrido post-order que retorna una cadena."""
        result = []
        self._traverse_post_order_helper(node, result)
        return " ".join(result)
    
    def _traverse_post_order_helper(self, node, result):
        if node:
            self._traverse_post_order_helper(node.left, result)
            self._traverse_post_order_helper(node.right, result)
            result.append(str(node.value))

    def search(self,value):
        return self.searchrec(self.root, value)
        
        
    def searchrec(self, node, value):
        """Busca un valor en el árbol."""
        if node is None:
            return None
        elif node.value == value:
            return node
        elif value <= node.value:
            return self.searchrec(node.left, value)
        else:
            return self.searchrec(node.right, value)


