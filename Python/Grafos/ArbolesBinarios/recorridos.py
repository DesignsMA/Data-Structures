import matplotlib.pyplot as plt

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


# === MAIN ===

tree = BinarySearchTre()
c = int(input("¿Cuántos números quieres tener en el árbol?: "))

for i in range(c):
    valor = int(input(f"Ingrese el valor #{i+1}: "))
    tree.add(valor)

while True:
    print("\n--- MENÚ ---")
    print("1. Mostrar recorrido in-order")
    print("2. Mostrar recorrido pre-order")
    print("3. Mostrar recorrido post-order")
    print("4. Buscar un valor")
    print("5. Salir")

    opcion = input("Elige una opción (1-5): ")

    if opcion == "1":
        print("\nRecorrido in-order:")
        tree.show_in_order(tree.root)
        tree.draw_tree()
    elif opcion == "2":
        print("\nRecorrido pre-order:")
        tree.show_pre_order(tree.root)
        tree.draw_tree()
    elif opcion == "3":
        print("\nRecorrido post-order:")
        tree.show_pos_order(tree.root)
        tree.draw_tree()
    elif opcion == "4":
        buscar = int(input("¿Qué valor quieres buscar?: "))
        nodo = tree.search(tree.root, buscar)
        if nodo:
            print(f"El valor {buscar} SÍ está en el árbol.")
        else:
            print(f"El valor {buscar} NO está en el árbol.")
        tree.draw_tree()
    elif opcion == "5":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")