class NodoB:
    def __init__(self, order:int):
        self.order = order
        self.keys = [] # claves
        self.nKeys = 0
        
        self.children = [] # hijos
        self.nChildren = 0
        
    @property
    def is_leaf(self):
        return self.nChildren == 0

class B_Tree():
    def __init__(self, order: int = 6 ):
        self.root = None
        self.m = order
    
    def search(self, node: NodoB, value):
        """Busca entre las claves contenidas en node.
        
        Si no lo encuentra, saltar al hijo donde puede estar.
        
        Si el nodo es hoja, el valor no existe.
        """
        if node is None: # si esta vacio
            return None
        # Búsqueda en el nodo actual
        keys = node.keys
        if len(keys) <= 10:  # Búsqueda lineal para nodos pequeños
            for i, key in enumerate(keys):
                if value == key: # verifica existencia
                    return node
                if value < key: # se encuentra en un hijo
                    return self.search(node.children[i], value) if not node.is_leaf else None # si el hijo no es hoja
            # Si value > todas las claves
            return self.search(node.children[-1], value) if not node.is_leaf else None
        
        # Búsqueda binaria para nodos grandes
        else: 
            left, right = 0, len(keys) - 1
            while left <= right:
                mid = (left + right) // 2
                if keys[mid] == value:
                    return node
                elif keys[mid] < value:
                    left = mid + 1
                else:
                    right = mid - 1
            # Decide el hijo a explorar
            return self.search(node.children[left], value) if not node.is_leaf else None
