from .persona import Persona

estados = {0: "Pendiente", 1: "Resuelto"}
class ProcesoLegal:
    """
    Representación de un proceso legal.
    
    Atributos de instancia:
        estado (str): Estado del caso | Pendiente - Resuelto.
        nombre (str): Nombre del repatriado.
        id (str): ID del repatriado.
        motivo (str): Motivo del desplazamiento.
    """
    def __init__(self, persona: Persona):
        """
        Args:
            persona (Persona): Persona que abre el caso.        
        """
        self.estado = estados[0]
        self.nombre = persona.nombre
        self.id = persona.id
        self.nacionalidad = persona.nacionalidad
        self.motivo = persona.motivo

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
            f"Motivo: {self.motivo}\n"
        )
        
