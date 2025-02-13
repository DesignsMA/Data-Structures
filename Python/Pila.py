class Pila:
    def _init_(self):
        self.items = []  # Usamos una lista para almacenar los elementos de la pila

    def esta_vacia(self):
        return len(self.items) == 0  # Verifica si la pila está vacía

    def push(self, elemento):
        self.items.append(elemento)  # Agrega un elemento a la pila

    def pop(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")  # Lanza una excepción si la pila está vacía
        return self.items.pop()  # Elimina y devuelve el último elemento de la pila

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")  # Lanza una excepción si la pila está vacía
        return self.items[-1]  # Devuelve el último elemento sin eliminarlo

    def tamano(self):
        return len(self.items)  # Devuelve el tamaño de la pila

    def _str_(self):
        return str(self.items)  # Representación en cadena de la pila