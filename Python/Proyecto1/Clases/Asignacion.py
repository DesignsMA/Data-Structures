from Persona import Persona

class Asignacion:
    """Representa la asignación de un recurso a un beneficiario.

    Atributos de instancia:
        tipo (str): Tipo de recurso asignado.
        nombre (str): Nombre del beneficiario, obtenido de la instancia de Persona.
        id: Identificador del beneficiario, obtenido de la instancia de Persona.
        nacionalidad (str): Nacionalidad del beneficiario, obtenido de la instancia de Persona.
        cantidad (int): Cantidad del recurso asignado.
    """
    
    def __init__(self, tipo: str, receptor: Persona, cantidad: int):
        """Inicializa una nueva asignación de recurso a un beneficiario.

        Args:
            tipo (str): Tipo de recurso que se asigna.
            receptor (Persona): Instancia de Persona que recibirá el recurso.
            cantidad (int): Cantidad del recurso asignado.
        """
        self.tipo = tipo
        self.nombre = receptor.nombre
        self.id = receptor.id
        self.nacionalidad = receptor.nacionalidad
        self.cantidad = cantidad

    def __str__(self):
        """Genera una representación en forma de cadena de la asignación.

        Returns:
            str: Cadena con los detalles de la asignación.
        """
        return (
            f"Tipo de recurso: {self.tipo}\n"
            f"Asignatario: {self.nombre}\n"
            f"ID: {self.id}\n"
            f"Nacionalidad: {self.nacionalidad}\n"
            f"Cantidad: {self.cantidad}\n"
        )
