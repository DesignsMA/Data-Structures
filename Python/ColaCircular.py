class ColaCircular:
    def _init_(self, capacidad):
        self.capacidad = capacidad  # Tamaño máximo de la cola
        self.cola = [None] * capacidad  # Arreglo para almacenar los elementos
        self.frente = 0  # Índice del frente de la cola
        self.final = -1  # Índice del final de la cola
        self.tamano = 0  # Número de elementos en la cola

    def esta_vacia(self):
        return self.tamano == 0  # Verifica si la cola está vacía

    def esta_llena(self):
        return self.tamano == self.capacidad  # Verifica si la cola está llena

    def encolar(self, elemento):
        if self.esta_llena():
            print("La cola está llena. No se puede encolar más elementos.")
            return
        # Calcula el índice circular para el final
        self.final = (self.final + 1) % self.capacidad
        self.cola[self.final] = elemento  # Agrega el elemento al final
        self.tamano += 1  # Incrementa el tamaño de la cola

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía. No se puede desencolar.")
        elemento = self.cola[self.frente]  # Obtiene el elemento del frente
        self.cola[self.frente] = None  # Elimina el elemento del frente
        self.frente = (self.frente + 1) % self.capacidad  # Mueve el frente circularmente
        self.tamano -= 1  # Reduce el tamaño de la cola
        return elemento

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self.cola[self.frente]  # Devuelve el elemento del frente sin eliminarlo

    def _str_(self):
        return str(self.cola)  # Representación en cadena de la cola