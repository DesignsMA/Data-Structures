import bisect
import matplotlib.pyplot as plt

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
        """Dibuja un nodo del B-Tree y sus conexiones con los hijos."""
        if node is not None:
            # Dibuja el rectángulo del nodo
            self.ax.text(x, y, str(node.keys), 
                        ha='center', va='center',
                        bbox=dict(facecolor='skyblue', boxstyle='round,pad=0.5'))

            if not node.is_leaf:
                # Calcula posiciones de los hijos
                num_children = len(node.children)
                total_width = min(num_children * dx, 15)  # Limita el ancho máximo
                start_x = x - total_width/2

                # Calcula el ancho por clave
                key_spacing = total_width / (len(node.keys) + 4)

                for i, child in enumerate(node.children):
                    child_x = start_x + i * (total_width / (num_children - 1)) if num_children > 1 else x

                    # Calcula posición de origen de la línea (centrada entre claves)
                    if i == 0:
                        line_x = x - (len(node.keys) * key_spacing)/2
                    else:
                        line_x = x - (len(node.keys) * key_spacing)/2 + i * key_spacing

                    # Dibuja línea de conexión
                    self.ax.plot([line_x, child_x], [y-0.1, y-0.9], 'k-', lw=1)

                    # Dibuja hijo recursivamente
                    self._draw_node(child, child_x, y-1, dx/2)

    def close_figure(self):
        """Cierra la figura de matplotlib."""
        if self.fig and plt.fignum_exists(self.fig.number):
            plt.close(self.fig)
            self.fig = None
            self.ax = None
    
    def traverse_in_order(self, node):
        """Recorrido in-order del árbol."""
        if node:
            self.mraverse_in_order(node.left)
            print(node.keys)
            self.mraverse_in_order(node.right)

    def traverse_pre_order(self, node):
        """Recorrido pre-order del árbol."""
        if node:
            print(node.keys)
            self.mraverse_pre_order(node.left)
            self.mraverse_pre_order(node.right)

    def traverse_post_order(self, node):
        """Recorrido post-order del árbol."""
        if node:
            self.mraverse_post_order(node.left)
            self.mraverse_post_order(node.right)
            print(node.keys)

    def search(self, node, value):
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
                    return self.search(node.children[i], value) if not node.is_leaf else None # si el hijo no es hoja
            # Si value > todas las claves
            return self.search(node.children[-1], value) if not node.is_leaf else None
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
            return self.search(node.children[left], value) if not node.is_leaf else None



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
                    tree.root = BTreeNode(5, True)
                    for num in numbers:
                        tree.insert(num)
                    tree.update_drawing()
            except Exception as e:
                print(f"Error: {e}")
        elif option == "4":
            tree.close_figure()
            break


def traversal_menu(tree):
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
    tree = BTree(5)
    
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