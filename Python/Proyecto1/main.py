from Clases import * # Necesita __init__.py para funcionar
from Estructuras import *
from Scripts.PolinomioDireccionamiento import polinomio_direccionamiento

class GestionAyuda():
    #Variables de clase, compartidas entre clases
    
    def __init__(self):
        #Variables de instancia, unicas de instancia
        self.registros = Cola() # Instancia de cola lineal
        self.urgentes = Pila() # Instancia de pila
        self.recursos = Lista() # Instancia de lista
        self.asignaciones = ListaDoble()