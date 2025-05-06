import matplotlib.pyplot as plt
import json
import os
plt.ion()  # Activar modo interactivo
class Nodo:
    def __init__(self, value=None, parent=None, is_root=False, is_left=False, is_right=False):
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent
        self.is_root = is_root
        self.is_left = is_left
        self.is_right = is_right
        


class BinarySearchTre:
    def __init__(self):
        self.root = None
        self.fig = None
        self.ax = None

    def empty(self):
        return self.root is None

    def add(self, value):
        if self.empty():
            self.root = Nodo(value=value, is_root=True)
        else:
            nodo = self.get_place(value)
            if value <= nodo.value:
                nodo.left = Nodo(value=value, parent=nodo, is_left=True)
            else:
                nodo.right = Nodo(value=value, parent=nodo, is_right=True)

    def get_place(self, valor):
        aux = self.root
        while aux is not None:
            temp = aux
            if valor <= aux.value:
                aux = aux.left
            else:
                aux = aux.right
        return temp

    def delete(self, valor):
        self.root = self._delete_rec(self.root, valor)

    def _delete_rec(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.value:
            nodo.left = self._delete_rec(nodo.left, valor)
        elif valor > nodo.value:
            nodo.right = self._delete_rec(nodo.right, valor)
        else:
            if nodo.left is None:
                return nodo.right
            elif nodo.right is None:
                return nodo.left
            temp = self._min_value_node(nodo.right)
            nodo.value = temp.value
            nodo.right = self._delete_rec(nodo.right, temp.value)
        return nodo

    def _min_value_node(self, nodo):
        actual = nodo
        while actual.left is not None:
            actual = actual.left
        return actual

    def show_in_order(self, nodo):
        if nodo:
            self.show_in_order(nodo.left)
            print(nodo.value)
            self.show_in_order(nodo.right)

    def show_pos_order(self, nodo):
        if nodo:
            self.show_pos_order(nodo.left)
            self.show_pos_order(nodo.right)
            print(nodo.value)

    def show_pre_order(self, nodo):
        if nodo:
            print(nodo.value)
            self.show_pre_order(nodo.left)
            self.show_pre_order(nodo.right)

    def search(self, nodo, valor):
        if nodo is None:
            return None
        elif nodo.value == valor:
            return nodo
        elif valor <= nodo.value:
            return self.search(nodo.left, valor)
        else:
            return self.search(nodo.right, valor)

    def draw_tree(self):
        fig, ax = plt.subplots()
        ax.axis("off")

        def draw_node(nodo, x, y, dx):
            if nodo is not None:
                ax.text(x, y, str(nodo.value), ha='center', bbox=dict(facecolor='skyblue', boxstyle='circle'))
                if nodo.left:
                    ax.plot([x, x - dx], [y, y - 1], 'k-')
                    draw_node(nodo.left, x - dx, y - 1, dx / 2)
                if nodo.right:
                    ax.plot([x, x + dx], [y, y - 1], 'k-')
                    draw_node(nodo.right, x + dx, y - 1, dx / 2)

        draw_node(self.root, x=0, y=0, dx=1.5)
        plt.title("Árbol Binario de Búsqueda")
        plt.show()

    def actualizar_dibujo(self):
        if self.fig is None or not plt.fignum_exists(self.fig.number):
            self.fig, self.ax = plt.subplots()
            self.fig.show()  # Mostrar figura explícitamente

        else:
            self.ax.clear()

        self.ax.axis("off")

        def draw_node(nodo, x, y, dx):
            if nodo is not None:
                self.ax.text(x, y, str(nodo.value), ha='center', bbox=dict(facecolor='skyblue', boxstyle='circle'))
                if nodo.left:
                    self.ax.plot([x, x - dx], [y, y - 1], 'k-')
                    draw_node(nodo.left, x - dx, y - 1, dx / 2)
                if nodo.right:
                    self.ax.plot([x, x + dx], [y, y - 1], 'k-')
                    draw_node(nodo.right, x + dx, y - 1, dx / 2)

        draw_node(self.root, x=0, y=0, dx=1.5)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def cerrar_figura(self):
        if self.fig and plt.fignum_exists(self.fig.number):
            plt.close(self.fig)
            self.fig = None
            self.ax = None

def menu_edicion(tree):
    while True:
        print("\n--- MENÚ DE EDICIÓN ---")
        print("1. Insertar un elemento")
        print("2. Eliminar un elemento")
        print("3. Cargar árbol desde archivo .txt")
        print("4. Volver al menú principal")

        opcion = input("Elige una opción: ")
    
        if opcion == "1":
            valor = int(input("Valor a insertar: "))
            tree.add(valor)
            tree.actualizar_dibujo()
        elif opcion == "2":
            valor = int(input("Valor a eliminar: "))
            tree.delete(valor)
            tree.actualizar_dibujo()
        elif opcion == "3":
            ruta = input("Nombre del archivo txt (ej. arbol.txt): ").strip()
            base_dir = os.path.dirname(os.path.abspath(__file__))
            ruta_completa = os.path.join(base_dir, ruta)
            print(ruta_completa)
            if not os.path.isfile(ruta_completa):
                print("Archivo no encontrado.")
                continue
            try:
                with open(ruta_completa, 'r') as f:
                    contenido = f.read()
                    numeros = [int(x.strip()) for x in contenido.split(',') if x.strip().isdigit()]
                    if not numeros:
                        print("No se encontraron números válidos.")
                        continue
                    tree.root = None  # Reiniciar el árbol
                    for num in numeros:
                        tree.add(num)
                    tree.actualizar_dibujo()
            except Exception as e:
                print(f"Error cargando archivo: {e}")
        elif opcion == "4":
            tree.cerrar_figura()
            break
        else:
            print("Opción inválida.")

def menu_recorridos(tree):
    while True:
        print("\n--- MENÚ DE RECORRIDOS ---")
        print("1. In-order")
        print("2. Pre-order")
        print("3. Post-order")
        print("4. Buscar")
        print("5. Volver al menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            tree.show_in_order(tree.root)
            tree.actualizar_dibujo()
        elif opcion == "2":
            tree.show_pre_order(tree.root)
            tree.actualizar_dibujo()
        elif opcion == "3":
            tree.show_pos_order(tree.root)
            tree.actualizar_dibujo()
        elif opcion == "4":
            val = int(input("Valor a buscar: "))
            nodo = tree.search(tree.root, val)
            print(f"{val} {'sí' if nodo else 'no'} está en el árbol.")
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")

tree = BinarySearchTre()

while True:
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Editar árbol")
    print("2. Ver recorridos")
    print("3. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        menu_edicion(tree)
    elif opcion == "2":
        menu_recorridos(tree)
    elif opcion == "3":
        print("Saliendo...")
        tree.cerrar_figura()
        break
    else:
        print("Opción inválida.")