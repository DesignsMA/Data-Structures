import numpy as np
from numpy import linalg
from Estructuras import *
from pprint import pp
class Grafo():
    
    def __init__(self, vertices: list, matrizAdjacencia: np.ndarray = None):
        self.n = len(vertices)
        self.vertices = { vertices[i]: Lista() for i in range(len(vertices)) } # crear diccionario de vertices con su lista ligada
        self.listaVertices = [key for key in self.vertices.keys()]
        self.matrizAdjacencia = matrizAdjacencia
        self.matrizCaminos = None
        self.matricesCaminos = []
        
        if matrizAdjacencia.all() == None or matrizAdjacencia.shape != (self.n, self.n): #caso por defecto o error
            self.matrizAdjacencia = np.zeros((self.n, self.n), int)  # Crear matriz de nxn
            if matrizAdjacencia.shape != (self.n, self.n):
                print("La matriz deberia ser de nxn donde n es el numero de vertices.\nLa matriz esta vacia.")
        else:
            self.generarListasAdjacencia() # generar  listas de adjacencia a partir de la matriz
                
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
        for vertice, lista in self.vertices.items():  # Iterar sobre llaves y valores
            for n in range( lista.len() ): # por cada vertice, verificar cada elemento de su lista de adjacencia
                adj = lista.get_element_at(n)
                i = 0
                for key in self.listaVertices: #recorrer lista de llaves (columnas)
                    if key == adj: # si la llave en posicion i es igual al adjacente en posicion n de la lista
                        self.matrizAdjacencia[m,i] = 1 # Marcar como adjacente
                        break # si ya se encontro, salir
                    i+=1 # siguiente llave (columna)
            m+=1 # siguiente fila (vertice)
    
    def generarListasAdjacencia(self):
        m = 0
        for vertice, lista in self.vertices.items(): # recorrer diccionario
            i = 0
            for adj in self.matrizAdjacencia[m]: # recorrer cada elemento en la fila m
                if adj == 1:  # si esta marcado como adjacente
                    lista.insertEnd( self.listaVertices[i] ) #adjuntar en la lista de adjacencia del vertice
                    break
                i+=1
            m+=1
    
    def generarMatrizDeCaminos(self):
        caminos = self.matrizAdjacencia
        for n in range(1, self.n): # desde 1 hasta  n-1
            caminos = np.matmul( caminos, self.matrizAdjacencia, dtype= int)
            self.matricesCaminos.append(caminos) # generar matriz de caminos de longitud n+1
        
        self.matrizCaminos = self.matrizAdjacencia
        for matriz in self.matricesCaminos: # generar matriz de todos los caminos
            for m in range( self.n ):
                for n in range( self.n ):
                    self.matrizCaminos[m,n] = matriz[m,n] or self.matrizCaminos[m,n]
        
        
    def __str__(self):
        strO = '{\n'
        for vertice, lista in self.vertices.items():  # Iterar sobre claves y valores
            strO += f"  '{vertice}': {lista.__str__()},\n"  # Incluir clave y valor
        strO += '}'
        return strO

grafo = Grafo(['A', 'B', 'C'], np.array( [ [0, 1, 0], [0, 0, 1], [1, 0, 0] ], int ) )
print(grafo)
grafo.generarMatrizAdjacencia()
print(grafo.matrizAdjacencia)
grafo.generarMatrizDeCaminos()
pp(grafo.matricesCaminos)
pp(grafo.matrizCaminos)