import numpy as np
from Estructuras import *
class Grafo():
    
    def __init__(self, vertices: list = []):
        n = len(vertices)
        self.matrizAdjacencia = np.zeros((n, n))  # Crear matriz de nxn
        self.vertices = { vertices[i]: Lista() for i in range(len(vertices)) } # crear diccionario de vertices con su lista ligada
    
    def __str__(self):
        strO = '{\n'
        for vertice, lista in self.vertices.items():  # Iterar sobre claves y valores
            strO += f"  '{vertice}': {lista.__str__()},\n"  # Incluir clave y valor
        strO += '}'
        return strO

grafo = Grafo(['A', 'B', 'C', 'D'])
print(grafo.__str__())