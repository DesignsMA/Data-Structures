class Nodo:
    def __init__(self, data):
        self.data = data  # Dato del nodo
        self.sig = None   # Referencia al siguiente nodo

class Lista:
    def __init__(self):
        self.root = None  # La lista empieza vacía

    def insertEnd(self, data):
        """Inserta un nodo al final de la lista."""
        nuevo = Nodo(data)

        if self.root is None:
            self.root = nuevo  # Si la lista está vacía, el nuevo nodo es la raíz
        else:
            aux = self.root
            while aux.sig is not None:  # Recorrer hasta el final
                aux = aux.sig
            aux.sig = nuevo  # Insertar al final

    def print(self):
        """Imprime la lista completa."""
        current = self.root
        while current is not None:
            print(current.data, end=" -> ")
            current = current.sig
        print("None")
        

list = Lista()
list.insertEnd(-1)
list.insertEnd([-2,4,5]) #en python, una lista puede apuntar a diferentes tipos de objetos u datos
list.insertEnd(Lista())
list.print()