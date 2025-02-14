from .persona import Persona

estados = {0: "Pendiente", 1: "Resuelto"}
class ProcesoLegal:
    def __init__(self, persona):
        """:
        Args:
        """
        self.estado = estados[0]
        self.persona = persona

    def __str__(self):
        """Genera una representación en forma de cadena del caso.

        Returns:
            str: Cadena con los detalles de la asignación.
        """
        return (
            f"Estado del caso: {self.estado}\n"
            f"Nombre del repatriado: {self.nombre}\n"
            f"ID: {self.id}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
        )
        
