import matplotlib.pyplot as plt
import os
import math
class NodoB:
    """Nodo de un árbol-B."""
    def __init__(self, parent=None):
        self.keys = []      # Lista de claves ordenadas (valores)
        self.children = []  # Lista de referencias a hijos (nodos hijos)
        self.parent = parent  # Nodo padre (opcional, útil para operaciones de división)
    
    def insert_key(self, key):
        """Inserta una clave manteniendo el orden."""
        idx = self._find_key_index(key)
        self.keys.insert(idx, key) # inserta ANTES del indice
        return idx
    
    def _find_key_index(self, key):
        """Encuentra la posición donde debería ir la clave (búsqueda binaria)."""
        left, right = 0, len(self.keys) # toma todo el arreglo
        while left < right: # mientras no se alcanzen
            mid = (left + right) // 2 # mitad entera
            if self.keys[mid] < key: # si se debe colocar a la derecha
                left = mid + 1
            else:
                right = mid # si no tomar la parte izquierda
        return left
    
    def insert_child(self, child, index):
        """Inserta un hijo en la posición especificada."""
        self.children.insert(index, child)
        if child is not None:
            child.parent = self
    
    @property
    def is_leaf(self):
        """Retorna True si el nodo es una hoja (no tiene hijos)."""
        return len(self.children) == 0

class B_Tree:
    """Implementación de un árbol binario de búsqueda con visualización."""
    def __init__(self, m: int = 6):
        self.root = None
        self.m = m
        self.minKeys = (m-1)/2 # N parte entera
        self.maxKeys = m-1 # L
        self.minChild = math.ceil(m/2.0) # redondeo
        self.fig = None     # Figura de matplotlib para visualización
        self.ax = None      # Ejes de matplotlib
        
    def add(self, key):
        """Añade una nueva clave al árbol."""
        if self.root is None: # si esta vacio
            self.root = NodoB() # añadir raiz, la raiz tiene de 1-m-1
            self.root.keys.append(key) # añadir key
        else:
            parent = self._find_parent(value)
            if value <= parent.value:
                parent.left = Nodo(value, parent)
            else:
                parent.right = Nodo(value, parent)

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
        elif value in node.keys: 
            return node # si esta retornar nodo donde se encontro
        elif not node.is_leaf: # si no es hoja
            for i in range(len(node.keys)): # encontrar el hijo
                if value < node.keys[i]: # si se podria encontrar en el hijo actual
                    return self.search(node.children[i]) # buscar
                
                if i == (len(node.keys)-1) and value > node.keys[i]: # si se esta en el ultimo hijo
                    return self.search(node.children[i+1]) # buscar en el ultimo hijo
        else:
            return None

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