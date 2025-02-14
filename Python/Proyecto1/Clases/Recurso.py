# Definición de los tipos de recursos disponibles
tipos = {0: "Alimentos", 1: "Refugios", 2: "Asesoría Legal"}

class Recurso:
    """
    Representación de un recurso disponible.

    Atributos de instancia:
        tipo (int): Tipo de recurso:
                    0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal
        
        cantidad (int): Número de recursos de este tipo disponibles.
        
        usados (int): Cantidad de recursos usados.
    """
    def __init__(self, tipo: int, cantidad: int):
        """
        Args:
            tipo (int): Tipo de recurso:
                        0 - Alimentos | 1 - Refugios | 2 - Asesoría Legal
            cantidad (int): Número de recursos de este tipo disponibles.

        Raises:
            ValueError: Si la cantidad es invalida.
        
        """
        if tipo not in tipos:
            raise ValueError(f"Tipo de recurso no válido. Opciones: {list(tipos.keys())}")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        
        self.tipo = tipos[tipo]  # Asigna el nombre del tipo de recurso
        self.cantidad = cantidad  # Asigna la cantidad disponible
        self.usados =  0 # inicializando  usados

    def __str__(self):
        """
        Representación en cadena del recurso.
        """
        return f"Recurso: {self.tipo} | Disponibles: {self.cantidad}"

    def usar(self, cantidad_usada: int):
        """
        Reduce la cantidad de recursos disponibles al usarlos.

        Args:
            cantidad_usada (int): Cantidad de recursos que se van a usar.

        Raises:
            ValueError: Si la cantidad usada es mayor que la disponible.
        """
        if cantidad_usada > self.cantidad:
            raise ValueError(f"No hay suficientes recursos. Disponibles: {self.cantidad}")
        self.cantidad -= cantidad_usada
        self.usados += 1 # solo si se usa

    def agregar(self, cantidad_agregada: int):
        """
        Aumenta la cantidad de recursos disponibles.

        Args:
            cantidad_agregada (int): Cantidad de recursos que se van a agregar.

        Raises:
            ValueError: Si la cantidad agregada es negativa.
        """
        if cantidad_agregada < 0:
            raise ValueError("La cantidad agregada no puede ser negativa.")
        self.cantidad += cantidad_agregada