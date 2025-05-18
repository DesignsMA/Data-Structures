class NodoAVL:
    """NodoAVL de un árbol AVL (con altura y factor de balance)."""
    def __init__(self, value=None, parent=None):
        self.value = value
        self.height = 0      # Altura inicializada en 0 (hoja)
        self.fb = 0          # Factor de balance inicial
        self.left = None     # Subárbol izquierdo
        self.right = None    # Subárbol derecho
        self.parent = parent # NodoAVL padre

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

    def empty(self):
        """Verifica si el árbol está vacío."""
        return self.root is None

    def insert(self, value):
        """Añade un nuevo valor al árbol."""
        new_node = None
        if self.empty():
            self.root = NodoAVL(value)
        else:
            parent = self._find_parent(value)
            new_node = NodoAVL(value, parent)
            if value <= parent.value:
                parent.left = new_node
            else:
                parent.right = new_node
        
        self._balance_tree(new_node)
        
    def _balance_tree(self, node: NodoAVL):
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
    
    def _rotate(self, p2: NodoAVL, new_node: NodoAVL):
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

    def _simple_rotation(self, p1: NodoAVL, p2: NodoAVL, p3: NodoAVL, new_node: NodoAVL):
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
    
    def _double_rotation(self, p1: NodoAVL, p2: NodoAVL, p3: NodoAVL, p4: NodoAVL, new_node: NodoAVL):
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
    
    def _update_bf_upwards(self, from_node: NodoAVL, to_node: NodoAVL):
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
            tree.insert(value)
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
                        tree.insert(num)
                    tree.update_drawing()
            except Exception as e:
                print(f"Error: {e}")
        elif option == "4":
            tree.close_figure()
            break


