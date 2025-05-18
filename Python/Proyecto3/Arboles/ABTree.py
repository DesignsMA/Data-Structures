from collections import deque

class NodoBinario:
    def __init__(self, value=None, parent=None):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

class BinaryTree:
    def __init__(self):
        self.root = None

    def empty(self):
        return self.root is None

    def insert(self, value):
        new_node = NodoBinario(value)
        if self.root is None:
            self.root = new_node
            return

        queue = deque([self.root])
        while queue:
            node = queue.popleft()

            # Insertar a la izquierda si está vacío
            if node.left is None:
                node.left = new_node
                new_node.parent = node
                return
            else:
                queue.append(node.left)

            # Insertar a la derecha si está vacío
            if node.right is None:
                node.right = new_node
                new_node.parent = node
                return
            else:
                queue.append(node.right)

    def search(self, value):
        if self.root is None:
            return None

        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.value == value:
                return node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return None

    def delete(self, value):
        if self.root is None:
            return

        queue = deque([self.root])
        node_to_delete = None
        last_node = None

        while queue:
            last_node = queue.popleft()
            if last_node.value == value:
                node_to_delete = last_node
            if last_node.left:
                queue.append(last_node.left)
            if last_node.right:
                queue.append(last_node.right)

        if node_to_delete:
            node_to_delete.value = last_node.value
            self._remove_last_node(last_node)

    def _remove_last_node(self, node):
        """Elimina el último nodo encontrado por nivel (para mantener estructura completa)."""
        parent = node.parent
        if parent:
            if parent.right == node:
                parent.right = None
            elif parent.left == node:
                parent.left = None
        elif self.root == node:
            self.root = None  # árbol vacío

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