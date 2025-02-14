from ..Clases.NodoDoble import *

class ListaDoble:
    def __init__(self):
        self.root = None  # La lista empieza vacía
        self.tail = None  # La cola también empieza vacía
        self.current = None  # Puntero al nodo actual

    def insertEnd(self, data):
        """Inserta un NodoDoble al final de la lista."""
        new = NodoDoble(data)

        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo NodoDoble es la raíz y la cola
            self.current = self.root  # El nodo actual es la raíz
        else:
            self.tail.sig = new  # El último NodoDoble apunta al nuevo NodoDoble
            new.ant = self.tail  # El nuevo NodoDoble apunta al NodoDoble anterior (cola)
            self.tail = new  # La cola se actualiza al nuevo NodoDoble

    def insertStart(self, data):
        """Inserta un NodoDoble al inicio de la lista."""
        new = NodoDoble(data)
        if self.root is None:
            self.root = self.tail = new  # Si la lista está vacía, el nuevo NodoDoble es la raíz y la cola
            self.current = self.root  # El nodo actual es la raíz
        else:
            new.sig = self.root  # El nuevo NodoDoble apunta al NodoDoble raíz
            self.root.ant = new  # El NodoDoble raíz apunta al nuevo NodoDoble
            self.root = new  # La raíz se actualiza al nuevo NodoDoble
            self.current = self.root  # El nodo actual es la nueva raíz

    def insertBetween(self, prev_data, data):
        """Inserta un NodoDoble después de un NodoDoble con el valor prev_data."""
        aux = self.root
        while aux is not None and aux.data != prev_data:
            aux = aux.sig

        if aux is None:
            print("Elemento previo no encontrado.")
        else:
            new = NodoDoble(data)
            new.sig = aux.sig  # El nuevo NodoDoble apunta al siguiente NodoDoble
            if aux.sig is not None:  # Si no estamos insertando al final
                aux.sig.ant = new  # El siguiente NodoDoble apunta al nuevo NodoDoble
            aux.sig = new  # El NodoDoble previo apunta al nuevo NodoDoble
            new.ant = aux  # El nuevo NodoDoble apunta al NodoDoble previo

    def remove(self, data: str):
        """Elimina un NodoDoble con el valor dado."""
        if self.root is None:
            print("Lista vacía.")
            return

        if self.root.data == data or data == "inicio":
            self.root = self.root.sig
            if self.root:  # Si no es el último NodoDoble
                self.root.ant = None
            self.current = self.root  # Actualizar el nodo actual
            return

        aux = self.root
        if data != "final":
            while aux.sig is not None and aux.sig.data != data:
                aux = aux.sig
        elif data == "final":
            while aux.sig.sig is not None:  # Recorrer hasta el penúltimo
                aux = aux.sig

        if aux.sig is None:
            print("Elemento no encontrado.")
        else:
            if aux.sig.sig is not None:
                aux.sig.sig.ant = aux  # El siguiente NodoDoble apunta al NodoDoble anterior
            aux.sig = aux.sig.sig  # El NodoDoble anterior apunta al siguiente de su siguiente
            if self.current == aux.sig:  # Si el nodo actual fue eliminado
                self.current = aux  # Actualizar el nodo actual al anterior

    def exists(self, data):
        """Verifica si un elemento está en la lista."""
        aux = self.root
        while aux is not None:
            if aux.data == data:
                return True
            aux = aux.sig
        return False

    def print(self):
        """Imprime la lista completa."""
        current = self.root
        while current is not None:
            print(current.data, end=" <-> ")
            current = current.sig
        print("None")

    def next(self):
        """Avanza al siguiente nodo y retorna su valor."""
        if self.current is None:
            print("Lista vacía.")
            return None
        if self.current.sig is None:
            print("Ya estás en el último elemento.")
            return self.current.data
        self.current = self.current.sig  # Avanzar al siguiente nodo
        return self.current.data  # Retornar el valor del nodo actual

    def prev(self):
        """Retrocede al nodo anterior y retorna su valor."""
        if self.current is None:
            print("Lista vacía.")
            return None
        if self.current.ant is None:
            print("Ya estás en el primer elemento.")
            return self.current.data
        self.current = self.current.ant  # Retroceder al nodo anterior
        return self.current.data  # Retornar el valor del nodo actual

    def current_element(self):
        """Retorna el valor del nodo actual."""
        if self.current is None:
            print("Lista vacía.")
            return None
        return self.current.data