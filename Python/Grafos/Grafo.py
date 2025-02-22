import numpy as np
from Estructuras import *
class Grafo():
    
    def __init__(self, vertices: list = []):
        self.n = len(vertices)
        self.matrizAdjacencia = np.zeros((self.n, self.n))  # Crear matriz de nxn
        self.vertices = { vertices[i]: Lista() for i in range(len(vertices)) } # crear diccionario de vertices con su lista ligada
    
    def definirAdjacencia(self):
        # Recorrer cada vértice y su lista de adyacencia
        for vertice, lista in self.vertices.items():
            print(f"\nDefiniendo adyacencias para el vértice: '{vertice}'")
            print("Vértices disponibles:", list(self.vertices.keys()))

            while True:
                adj = input(f"Ingresa un vértice adyacente a '{vertice}' (-1 para terminar): ").strip()  # Eliminar espacios en blanco

                if adj == "-1":
                    break  # Salir del bucle para este vértice
                
                if adj in self.vertices:  # Verificar si el vértice adyacente existe
                    if not lista.exists(adj):  # Evitar duplicados
                        lista.insertEnd(adj)  # Agregar a la lista de adyacencia
                        print(f"'{adj}' agregado como adyacente a '{vertice}'.")
                    else:
                        print(f"'{adj}' ya está en la lista de adyacencia de '{vertice}'.")
                else:
                    print(f"Error: '{adj}' no es un vértice válido.")

    def generarMatrizAdjacencia(self):
        m = 0
        for vertice, lista in self.vertices.items():  # Iterar sobre claves y valores
            for n in range( lista.len() ): # por cada fila, recorrer longitud de la lista columnas
                self.matrizAdjacencia[m,n] =
        
    
    def __str__(self):
        strO = '{\n'
        for vertice, lista in self.vertices.items():  # Iterar sobre claves y valores
            strO += f"  '{vertice}': {lista.__str__()},\n"  # Incluir clave y valor
        strO += '}'
        return strO

grafo = Grafo(['A', 'B', 'C', 'D'])
print(grafo)
grafo.definirAdjacencia()
print(grafo)