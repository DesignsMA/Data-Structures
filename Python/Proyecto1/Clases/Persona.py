import uuid
import string

# Diccionario de prioridades
prioridades = {0: "Regular", 1: "Urgente"}

class Persona:
    def __init__(self, nombre: str, nacionalidad: str, motivo: str, prioridad: int = 0):
        """
        Representación de una persona.

        Args:
            nombre (str): Nombre completo de la persona.
            nacionalidad (str): Nacionalidad de la persona.
            motivo (str): Motivo del desplazamiento.
            prioridad (int): 0 - Regular | 1 - Urgente

        Raises:
            ValueError: Si la prioridad no es válida.
        """
        self.id = uuid.uuid4()  # Generar un ID único
        self.nombre = string.capwords(nombre)  # Formatear el nombre (cada palabra en mayúscula)
        self.nacionalidad = nacionalidad.capitalize()  # Formatear la nacionalidad
        self.motivo = motivo.capitalize()  # Formatear el motivo
        if prioridad not in prioridades:
            raise ValueError(f"Prioridad no válida. Opciones: {list(prioridades.keys())}")
        self.prioridad = prioridades[prioridad]  # Asignar la prioridad

    def __str__(self):
        """
        Representación en cadena de la persona.
        """
        return (
            f"ID: {self.id}\n"
            f"Nombre: {self.nombre}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
            f"Prioridad: {self.prioridad}\n"
            f"Motivo de desplazamiento: {self.motivo}"
        )
        
    def datosBasicos(self):
        """
        Datos básicos de una persona, nombre, id, nacionalidad
        """
        return (
            f"Nombre: {self.nombre}\n"
            f"ID: {self.id}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
        )