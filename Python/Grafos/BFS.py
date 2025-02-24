#Recorrido por amplitud
from Estructuras import Cola
from Grafo import Grafo

def bfs_amplitud(grafo: Grafo, inicio):
    espera = set()  # conjunto de vertices o nodos en espera
    cola = Cola()  # instancia de clase Cola
    cola.encolar(inicio) # encolar  (marcar como listo) al vertice inicial
    recorridoAmplitud = { grafo.listaVertices[i]: [] for i in range(grafo.n) } # diccionario de grafo resultante
    
    espera.update(recorridoAmplitud.keys()) # colocar vertices en espera
    espera.difference_update(inicio) # eliminar de la lista de espera | marcar listo
    
    while not cola.esta_vacia():  # Continua hasta que la cola esta vacía
        nodo = cola.desencolar()  # saca el nodo de la cola y lo almacena para ser usado despues
        print(nodo) # Imprime el nodo actual (para visualizar)
        for vertice in grafo.vertices[nodo]: #recorrer lista de vertices adyacentes al nodo
            if vertice in espera: # si el vertice actual esta en espera
                cola.encolar(vertice) # encolar vertice
                recorridoAmplitud[nodo].append(vertice) # añadir adyacentes en la lista del nodo
                espera.difference_update(vertice) # eliminar de la lista de espera | marcar listo
                
    return recorridoAmplitud


# Definimos el grafo mediante un diccionario de phyton

grafo = Grafo( diccionarioAdjacencia= {
    'V': ['R'],
    'R': ['S', 'V'],
    'S': ['R', 'W'],
    'W': ['T', 'X', 'S'],
    'T': ['W', 'X', 'U'],
    'X': ['T', 'Y', 'U', 'W'],
    'Y': ['X', 'U'],
    'U': ['T', 'X', 'Y'],
})
# Llamamos a a funcion que creamos dando inicio en el nodo "S"

res = Grafo( diccionarioAdjacencia=bfs_amplitud(grafo, 'S'))
print("Representación | Grafo del arbol resultante :\n")
print(res)


