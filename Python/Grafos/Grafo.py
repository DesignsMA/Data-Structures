import numpy as np
class Grafo():
    
    def __init__(n: int):
        matrizAdjacencia = np.zeros(n,n) #crear matriz de nxn