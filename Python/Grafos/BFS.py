#Recorrido por amplitud
import networkx as nx
G = nx.Graph()
from Estructuras import Cola
from Grafo import Grafo
from pprint import pp

def bfs_amplitud(grafo: Grafo, inicio):
    procesado = set()  # seguimiento de nodos procesados (aqui se irá viendo el orden del camino)
    cola = Cola()  # se usa una pila para la busqueda profunda inicializandola con el primer nodo(inicio)
    cola.encolar(inicio)
    recorridoAmplitud = { grafo.listaVertices[i]: [] for i in range(grafo.n) }

    while not cola.esta_vacia():  # Continua hasta que la cola esta vacía
        nodo = cola.desencolar()  # saca el nodo de la cola y lo almacena para ser usado despues
        procesado.add(nodo)  # Verifica el nodo añadiendolo al set para llevar el orden del camino
        print(nodo)        # Imrpime el nodo actual (para visualizar)
        for vertice in grafo.vertices[nodo]: #recorrer lista de vertices adyacentes
            if vertice not in procesado:
                cola.encolar(vertice) # encolar vertice
                recorridoAmplitud[nodo].append(vertice) # representar  el recorrido
    return recorridoAmplitud


# Definimos el grafo mediante un diccionario de phyton

grafo = Grafo( dictionarioAdjacencia= {
    'V': ['R'],
    'R': ['S'],
    'S': ['R', 'W'],
    'W': ['T', 'X'],
    'T': ['W', 'X', 'U'],
    'X': ['T', 'Y', 'U', 'W'],
    'Y': ['X', 'U'],
    'U': ['T', 'X', 'Y'],
})

# DFS o busqueda profunda
        
# Llamamos a a funcion que creamos dando inicio en el nodo "A"
pp(bfs_amplitud(grafo, 'S'))


