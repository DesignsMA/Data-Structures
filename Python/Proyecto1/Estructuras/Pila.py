class Pila:
    def __init__(self):
        """Inicializa una pila vacía."""
        self.lista = []  # Lista para almacenar los elementos de la pila
        self.tope = 0    # Contador para el número de elementos en la pila

    def empty(self):
        """Verifica si la pila está vacía."""
        return self.tope == 0  # Retorna True si no hay elementos, False en caso contrario

    def push(self, dato):
        """Agrega un elemento a la pila."""
        self.lista.append(dato)  # Agrega el elemento al final de la lista
        self.tope += 1           # Incrementa el contador de elementos

    def pop(self):
        """Elimina y retorna el elemento en la cima de la pila."""
        if self.empty():
            raise IndexError("La pila está vacía")  # Lanza una excepción si la pila está vacía
        self.tope -= 1           # Decrementa el contador de elementos
        return self.lista.pop()  # Elimina y retorna el último elemento de la lista

    def show(self):
        """Muestra los elementos de la pila."""
        if self.empty():
            print("La pila está vacía")
        else:
            for i in range(self.tope - 1, -1, -1):  # Recorre la lista en orden inverso
                print(f"[{i}] -> {self.lista[i]}")

    def size(self):
        """Retorna el número de elementos en la pila."""
        return self.tope

    def top(self):
        """Retorna el elemento en la cima de la pila sin eliminarlo."""
        if self.empty():
            raise IndexError("La pila está vacía")  # Lanza una excepción si la pila está vacía
        return self.lista[-1]  # Retorna el último elemento de la lista