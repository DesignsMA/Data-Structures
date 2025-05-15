import matplotlib.pyplot as plt
import os
import math
import math

class NodoB:
    """Nodo de un árbol-B."""
    def __init__(self, parent=None):
        self.keys = []
        self.children = []
        self.parent = parent

    @property
    def is_leaf(self):
        return len(self.children) == 0

class BTree:
    def __init__(self, order=6):
        self.order = order
        self.max_keys = order - 1
        self.min_keys = math.ceil(self.max_keys / 2)
        self.root = None

    def add(self, key):
        """
        Inserta una clave en el árbol B usando un enfoque recursivo.
        Si la raíz se divide, se crea una nueva raíz.
        """
        if self.root is None:
            self.root = NodoB()
            self.root.keys.append(key)
            return

        promo = self._insert(self.root, key)
        if promo:
            # División de la raíz
            new_root = NodoB()
            new_root.keys = [promo[0]]
            new_root.children = [promo[1], promo[2]]
            promo[1].parent = new_root
            promo[2].parent = new_root
            self.root = new_root

    def _insert(self, node, key):
        """
        Inserta recursivamente.
        Retorna:
          None si no hubo división,
          o (key_promoted, left_node, right_node) si el nodo se dividió.
        """
        # Encuentra posición de inserción
        idx = self._find_index(node.keys, key)

        if node.is_leaf:
            # Inserción en hoja
            node.keys.insert(idx, key)
        else:
            # Descender al hijo adecuado
            child = node.children[idx]
            promo = self._insert(child, key)
            if promo:
                # Integrar promoción del hijo
                k_prom, left, right = promo
                insert_idx = self._find_index(node.keys, k_prom)
                node.keys.insert(insert_idx, k_prom)
                node.children[insert_idx] = left
                node.children.insert(insert_idx + 1, right)
                left.parent = node
                right.parent = node

        # Verificar overflow
        if len(node.keys) > self.max_keys:
            return self._split(node)
        else:
            return None

    def _split(self, node):
        """
        Divide un nodo que excede max_keys.
        Retorna (mid_key, left_node, right_node).
        """
        mid = len(node.keys) // 2
        mid_key = node.keys[mid]

        left = NodoB(node.parent)
        left.keys = node.keys[:mid]
        right = NodoB(node.parent)
        right.keys = node.keys[mid+1:]

        # Si no es hoja, repartir hijos
        if node.children:
            left.children = node.children[:mid+1]
            right.children = node.children[mid+1:]
            for c in left.children:
                c.parent = left
            for c in right.children:
                c.parent = right

        return (mid_key, left, right)
    
    def delete(self,key,node: NodoB = None):
        if node is None:
            node = self.search(self.root, key)  # Buscar el nodo que contiene la clave

        if node is None:
            return  # Clave no encontrada, no hay nada que hacer

        if node.is_leaf:
            # CASO 1: Eliminar en hoja
            node.keys.remove(key)

            if len(node.keys) < self.min_keys:
                # CASO 3: El nodo quedó con pocas claves
                self._fix_underflow(node)

        else:
            # CASO 2: Eliminar en nodo interno

            idx = node.keys.index(key)

            left_child = node.children[idx]
            right_child = node.children[idx + 1]

            if len(left_child.keys) >= self.t:
                # Reemplazar con el predecesor (máximo del subárbol izquierdo)
                predecessor = self._get_max(left_child)
                node.keys[idx] = predecessor
                self.delete(left_child, predecessor)

            elif len(right_child.keys) >= self.t:
                # Reemplazar con el sucesor (mínimo del subárbol derecho)
                successor = self._get_min(right_child)
                node.keys[idx] = successor
                self.delete(right_child, successor)

            else:
                # Ningún hijo puede prestar → hacer fusión
                self._merge(node, idx)
                self.delete(left_child, key)

        # Debe verificar si la raíz actual está vacía:
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]
            self.root.parent = None

            
    def _fix_underflow(self, node:NodoB):
        "Arregla los casos donde faltan claves."
         # Encuentra posición de inserción
        parent = node.parent
        idx = parent.children.index(node) # recuperar indice del hijo
        if idx == 0:
            # Solo hermano derecho
            if len(parent.children[1].keys) > self.min_keys:
                self._leftRotation(node, parent, parent.children[1], 0)
            else:
                self._merge(parent, 0)  # fusiona node con children[1]
        elif idx == len(parent.children) - 1:
            # Solo hermano izquierdo
            if len(parent.children[idx - 1].keys) > self.min_keys:
                self._rightRotation(node, parent, parent.children[idx - 1], idx - 1)
            else:
                self._merge(parent, idx - 1)  # fusiona children[idx - 1] con node
        else:
            # Tiene ambos hermanos
            if len(parent.children[idx - 1].keys) > self.min_keys:
                self._rightRotation(node, parent, parent.children[idx - 1], idx - 1)
            elif len(parent.children[idx + 1].keys) > self.min_keys:
                self._leftRotation(node, parent, parent.children[idx + 1], idx)
            else:
                # Fusión con el izquierdo por convención
                self._merge(parent, idx - 1)
    
    def _merge(self, parent:NodoB, idx):
        """Fusiona los elementos del padre con el hijo izquierdo de indice idx.
           No actualiza el padre en caso de que sea la raíz
        """
        left = parent.children[idx]
        right = parent.children[idx+1]
        left.keys.append(parent.keys.pop(idx))
        left.keys.extend(right.keys) # ahora left contiene todas las claves

        if not left.is_leaf:
            left.children.extend(right.children)
            for child in right.children:
                child.parent = left

        parent.children.pop(idx + 1)
        
        # Verificar subflujo en el padre y corregir recursivamente
        if len(parent.keys) < self.min_keys:  # ¡Clave faltante en tu código!
            self._fix_underflow(parent)  # Llamada recursiva para corregir

            
    def _rightRotation(self, node: NodoB, parent: NodoB, leftChild: NodoB, demoted):
        demotedKey = parent.keys[demoted]  # clave que baja desde el padre

        # Insertar clave del padre en posición ordenada
        insert_idx = self._find_index(node.keys, demotedKey)
        node.keys.insert(insert_idx, demotedKey)

        # Nueva clave para el padre (mayor de leftChild)
        parent.keys[demoted] = leftChild.keys.pop()

        # Si tienen hijos, mover el hijo correspondiente
        if not node.is_leaf:
            moved_child = leftChild.children.pop() # hijo de mayores al mayor del hijo izquierdo
            node.children.insert(0, moved_child) # se inserta en el inicio del nodo interno
            
            #el padre baja demoted a node, el hijo izquierdo sube su clave mas grande
            # al padre, como se queda sin una clave su hijo correspondiente
            # pasa a node
            moved_child.parent = node

    def _leftRotation(self, node:NodoB, parent:NodoB, rightChild: NodoB, demoted):
        demotedKey = parent.keys[demoted] # clave del padre
        insert_idx = self._find_index(node.keys, demotedKey)
        node.keys.insert(insert_idx,demotedKey)  # insertar clave del padre
        
        parent.keys[demoted] = rightChild.keys.pop(0) # ahora el menor del derecho ocupa la clave que separa los hijos
        
        # Si tienen hijos, mover el hijo correspondiente
        if not node.is_leaf:
            moved_child = rightChild.children.pop(0) 
            node.children.append(moved_child)
            moved_child.parent = node
        
        
    @staticmethod
    def _find_index(keys, key):
        """Búsqueda binaria para índice de inserción."""
        low, high = 0, len(keys)
        while low < high:
            mid = (low + high) // 2
            if keys[mid] < key:
                low = mid + 1
            else:
                high = mid
        return low

    def traverse_in_order(self, node):
        """Recorrido in-order del árbol."""
        if node:
            self.traverse_in_order(node.left)
            print(node.keys)
            self.traverse_in_order(node.right)

    def traverse_pre_order(self, node):
        """Recorrido pre-order del árbol."""
        if node:
            print(node.keys)
            self.traverse_pre_order(node.left)
            self.traverse_pre_order(node.right)

    def traverse_post_order(self, node):
        """Recorrido post-order del árbol."""
        if node:
            self.traverse_post_order(node.left)
            self.traverse_post_order(node.right)
            print(node.keys)

    def search(self, node: NodoB, value):
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


def traversal_menu(tree: B_Tree):
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
    tree = B_Tree()
    
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