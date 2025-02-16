class Cola:
    def __init__(self):
        """Inicializa una cola vacía."""
        self.items = []  # Usamos una lista para almacenar los elementos de la cola

    def esta_vacia(self):
        """Verifica si la cola está vacía."""
        return len(self.items) == 0

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola."""
        self.items.append(elemento)

    def desencolar(self):
        """Elimina y devuelve el primer elemento de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items.pop(0)  # Elimina y devuelve el primer elemento de la cola

    def frente(self):
        """Devuelve el primer elemento de la cola sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")  # Lanza una excepción si la cola está vacía
        return self.items[0]

    def tamano(self):
        """Devuelve el número de elementos en la cola."""
        return len(self.items)

    def __str__(self):
        """Devuelve una representación en cadena de la cola."""
        return str(self.items)

    def vaciar(self):
        """Vacía la cola, eliminando todos los elementos."""
        self.items.clear()

    def copiar(self):
        """Devuelve una copia de la cola."""
        nueva_cola = Cola()
        nueva_cola.items = self.items.copy()
        return nueva_cola

    def contiene(self, elemento):
        """Verifica si un elemento está en la cola."""
        return elemento in self.items

    def invertir(self):
        """Invierte el orden de los elementos en la cola."""
        self.items.reverse()
    
    def show(self):
        """Retorna la representación en cadena de la cola, incluso para objetos personalizados."""
        return "[" + ", ".join(str(item) for item in self.items) + "]"