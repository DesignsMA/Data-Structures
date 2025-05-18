import bisect

class BTreeNode:
    """Nodo de Árbol-B acuerdo a la definición de Knuth """
    def __init__(self, m, is_leaf):
        """
        Inicializa un nodo de Árboles-B.

        Args:
            m: Orden del árbol (Máximo número de hijos)
            is_leaf: Booleano que indica si el nodo es una hoja.
        """
        self.keys = []          # List to store keys in the node
        self.m = m              # Order of the B-Tree (max children)
        self.children = []      # List to store child nodes
        self.is_leaf = is_leaf  # Whether this node is a leaf

    def is_full(self):
        """Checa si el nodo ha alcanzado su máximo número de claves (m-1)."""
        return len(self.keys) == self.m - 1

    def split(self):
        """
        Divide el nodo cuando esta lleno..

        Returns:
            tuple: (median_key, new_right_node)
        """
        median_index = (self.m - 1) // 2 # indice medio
        median_key = self.keys[median_index]

        # Nuevo nodo derecho, conserva el estado de hoja del original
        new_right_node = BTreeNode(self.m, self.is_leaf)

        # Dividir claves, claves que van despues del pivote o mediana van al nuevo
        new_right_node.keys = self.keys[median_index + 1:]
        self.keys = self.keys[:median_index] # el nodo actual se actualiza con solo las claves que estan antes del pivote

        if not self.is_leaf:
            # Dividir hijos, hijos que van despues del pivote se van al nuevo nodo
            new_right_node.children = self.children[median_index + 1:]
            self.children = self.children[:median_index + 1] # toma los hijos que van hasta el pivote (incluyente)
        
        return median_key, new_right_node

    def insert(self, new_key):
        """
        Inserta una clave en el subárbol de este nodo.

        Args:
            new_key: Clave a ser insertada

        Returns:
            tuple: (median_key, new_right_node) Si el nodo fue dividido, None de otra manera.
        """
        if new_key not in self.keys:
            new_child_node = None
    
            if not self.is_leaf:
                # Encuentra el hijo apropiado para la insercion, este hijo es el mismo a la posicion ordenada en el arreglo, por busqueda binaria
                # Verificar duplicados eficientemente
                insert_pos = bisect.bisect_left(self.keys, new_key)
                if insert_pos < len(self.keys) and self.keys[insert_pos] == new_key:
                    return None  # Clave duplicada, no insertar

    
                # Inserta recursivamente en el nodo hijo
                new_child_node = self.children[insert_pos].insert(new_key)
    
                if new_child_node is not None:
                    # Hijo fue dividido, se debe incorporar la clave media o pivote
                    if not self.is_full(): # si puede contenerlo
                        # Inserta pivote y apuntador al nuevo hijo
                        self.keys.insert(insert_pos, new_child_node[0])
                        self.children.insert(insert_pos + 1, new_child_node[1])
                        new_child_node = None # reiniciar hijo
                    else:
                        # El nodo actual esta lleno, separar tras la insercion
                        self.keys.insert(insert_pos, new_child_node[0])
                        self.children.insert(insert_pos + 1, new_child_node[1])
                        median_key, new_right_node = self.split()
                        return (median_key, new_right_node)
            else:
                # Insertar en nodo hoja
                # Verificar duplicados eficientemente
                insert_pos = bisect.bisect_left(self.keys, new_key)
                if insert_pos < len(self.keys) and self.keys[insert_pos] == new_key:
                    return None  # Clave duplicada, no insertar

                self.keys.insert(insert_pos, new_key)
    
                # Checar si el nodo hoja debe ser separado
                if len(self.keys) == self.m:
                    return self.split()
    
            return new_child_node # retornar el hijo si hubo division

    def create_new_root(self, median_key, new_right_node):
        """
        Crea una nueva raíz cuando la raíz fue dividida.

        Args:
            median_key: Clave a ser promovida como nueva raíz
            new_right_node: El nuevo hijo derecho

        Returns:
            BTreeNode: El nuevo nodo raíz
        """
        new_root = BTreeNode(self.m, False)
        new_root.keys.append(median_key)
        new_root.children.append(self)  # Nodo original se convierte en el nodo izquierdo
        new_root.children.append(new_right_node)
        return new_root

    def delete(self, key):
        index = bisect.bisect_left(self.keys, key)
        
        # caso 1, la clave fue enbcontrada en el nodo 
        if index < len(self.keys) and self.keys[index] == key:
            if self.is_leaf:
                self.delete_from_leaf(index)
            else:
                self.delete_from_internal(index)
        else:  # caso 2, la clave no  esta en el nodo
            if self.is_leaf:
                return None

            flag = (index == len(self.keys)) # la clave estaria en el subarbol derecho?
            
            # si el hijo tiene menos de m-1 claves, verificar underflow
            
            if len(self.children[index].keys) < self.m:
                self.fill_child(index)
            
            # si el ultimo hijo fue fusionado
            
            if flag and index > len(self.keys): # si ahora el nodo fue fusionado y disminuyo
                self.children[index-1].delete(key) # buscar en el hijo anterior
            else:
                self.children[index].delete(key) # busca normalmente y borra la clave

    def delete_from_leaf(self, index):
        "Elimina la clave en el indice dado de una hoja."
        self.keys.pop(index)
    
    def delete_from_internal(self, index):
        "Elimina la clave en el indice dado de un nodo itnerno."
        key = self.keys[index]
        
        # caso 3a, el hijo anterior tiene al menos m-1 claves
        if len(self.children[index].keys) >= self.m:
            predecessor = self.get_predecessor(index)
            self.keys[index] = predecessor # intercambiar por el predecesor
            self.children[index].delete(predecessor) # eliminar  duplicado
        
        # caso 3b, el hijo siguiente tiene al menos m-1 
        elif len(self.children[index+1].keys) >= self.m:
            successor = self.get_successor(index)
            self.keys[index] = successor # intercambiar por el sucesor
            self.children[index+1].delete(successor) # eliminar  duplicado

        #caso 3c, ambos hijos tienen m-1 claves
        else:
            self.merge(index)
            self.children[index].delete(key) # fusionar y eliminar clave
    
    def get_predecessor(self, index):
        """Obtiene el predecesor de la clave en el índice dado"""
        actual = self.children[index]
        while not actual.is_leaf:
            actual = actual.children[-1] # ultimo
        return actual.keys[-1]
    
    def get_successor(self, index):
        """Obtiene el sucesor de la clave en el índice dado"""
        actual = self.children[index+1]
        # recorre el subarbol derecho y retorna el menor de todos
        while not actual.is_leaf:
            actual = actual.children[0] # primero
        return actual.keys[0]
        
    def fill_child(self, index):
        """Llena un hijo que tiene menos de t-1 claves"""
        # Caso a: Tomar prestado del hermano anterior con claves
        if index != 0 and len(self.children[index-1].keys) >= self.m:
            self.borrow_previous(index)
        
        # Caso b: Tomar prestado del hermano siguiente con claves
        elif index != len(self.keys) and len(self.children[index+1].keys) >= self.m:
            self.borrow_next(index)
        
        # Caso c: Fusionar con un hermano
        else:
            if index != len(self.keys):
                self.merge(index)
            else:
                self.merge(index-1)

    def borrow_previous(self, index):
        child = self.children[index] # desde un nodo enraizado, tomar los hijos
        brother = self.children[index-1] # hermano previo
        # Desplazar claves e hijos del hijo hacia la derecha
        child.keys.insert(0, self.keys[index-1])
        if not child.es_hoja: # tiene hijos
            child.children.insert(0, brother.children.pop())
        
        # Mover clave del hermano al padre
        self.keys[index-1] = brother.keys.pop()
            
    def borrow_next(self, index):
        child = self.children[index]
        brother = self.children[index + 1]

        # Mover clave del padre al final del hijo
        child.keys.append(self.keys[index])

        # Mover primer hijo del hermano si no es hoja
        if not child.is_leaf:
            child.children.append(brother.children.pop(0))

        # Reemplazar clave del padre con la primera del hermano
        self.keys[index] = brother.keys.pop(0)
    
    def merge(self, index):
        """Fusiona el hijo[index] con el hijo[index+1]"""
        child = self.children[index]
        brother = self.children[index+1]
        # Mover clave del padre al hijo, el hijo es menor al padre[index]
        child.keys.append(self.keys.pop(index))
        # mover claves del hermano
        child.keys.extend(brother.keys)
        
        # si no es hoja
        
        if not child.is_leaf:
            child.children.extend(brother.children)
        
        self.children.pop(index+1) # eliminar hermano fusionado
    
class BTree:
    """B-Tree implementation following Knuth's definition"""
    def __init__(self, m:int=5):
        """
        Initialize B-Tree.

        Args:
            m: Order of the B-Tree (maximum number of children)
        """
        self.root = BTreeNode(m, True)
        self.m = m  # Order of the B-Tree (max children)

    def insert(self, key):
        """
        Inserta una clave en el Árbol-B

        Args:
            key: Clave a ser insertada.
        """
        split_result = self.root.insert(key) # prueba a insertar en el nodo raiz

        if split_result is not None:
            # Raíz fue dividida, crear nueva raíz
            median_key, new_right_node = split_result
            self.root = self.root.create_new_root(median_key, new_right_node)
    
    def delete(self, key):
        """
        Elimina una clave en el Árbol-B

        Args:
            key: Clave a ser eliminada.
        """
        self.root.delete(key)
        
        if len(self.root.keys) == 0:
            if self.root.is_leaf:
                self.root = None
            else:
                # la raiz tiene un hijo solamente
                self.root = self.root.children[0]

    def traverse_in_order(self, node):
        """Recorrido in-order para árbol B: hijos[i] -> clave[i] -> hijos[i+1]"""
        result = []
        if node:
            for i in range(len(node.keys)):
                if i < len(node.children):
                    result.append(self.traverse_in_order(node.children[i]))
                result.append(str(node.keys[i]))
            # último hijo
            if len(node.children) > len(node.keys):
                result.append(self.traverse_in_order(node.children[-1]))
        return ' '.join(filter(None, result))

    
    def traverse_pre_order(self, node):
        """Recorrido pre-order para árbol B: claves primero, luego todos los hijos"""
        result = []
        if node:
            result.append(' '.join(str(k) for k in node.keys))
            for child in node.children:
                result.append(self.traverse_pre_order(child))
        return ' '.join(filter(None, result))

    def traverse_post_order(self, node):
        """Recorrido post-order para árbol B: primero los hijos, luego las claves"""
        result = []
        if node:
            for child in node.children:
                result.append(self.traverse_post_order(child))
            result.append(' '.join(str(k) for k in node.keys))
        return ' '.join(filter(None, result))


    def search(self,value):
        return self.searchrec(self.root, value)
        
    def searchrec(self, node, value):
        """Busca un valor en el árbol."""
        if node is None: # si esta vacio
            return None
        
            # Búsqueda en el nodo actual
        keys = node.keys
        if len(keys) <= 10:  # Búsqueda secuencial para nodos pequeños
            for i, key in enumerate(keys):
                if value == key: # verifica existencia
                    return node
                if value < key: # se encuentra en un hijo
                    return self.searchrec(node.children[i], value) if not node.is_leaf else None # si el hijo no es hoja
            # Si value > todas las claves
            return self.searchrec(node.children[-1], value) if not node.is_leaf else None
        else:  # Búsqueda binaria para nodos grandes
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
            return self.searchrec(node.children[left], value) if not node.is_leaf else None

