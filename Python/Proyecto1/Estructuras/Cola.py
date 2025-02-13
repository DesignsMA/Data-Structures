class Cola:
    def _init_(self):
        self.items = []  # Usamos una lista para almacenar los elementos de la cola

    def esta_vacia(self):
        return len(self.items) == 0  # Verifica si la cola está vacía

    def encolar(self, elemento):
        self.items.append(elemento)  # Agrega un elemento al final de la cola

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items.pop(0)  # Elimina y devuelve el primer elemento de la cola

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items[0]  # Devuelve el primer elemento sin eliminarlo

    def tamano(self):
        return len(self.items)  # Devuelve el tamaño de la cola

    def _str_(self):
        return str(self.items)  # Representación en cadena de la colaclass Cola:
    def _init_(self):
        self.items = []  # Usamos una lista para almacenar los elementos de la cola

    def esta_vacia(self):
        return len(self.items) == 0  # Verifica si la cola está vacía

    def encolar(self, elemento):
        self.items.append(elemento)  # Agrega un elemento al final de la cola

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items.pop(0)  # Elimina y devuelve el primer elemento de la cola

    def frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items[0]  # Devuelve el primer elemento sin eliminarlo

    def tamano(self):
        return len(self.items)  # Devuelve el tamaño de la cola

    def _str_(self):
        return str(self.items)  # Representación en cadena de la cola