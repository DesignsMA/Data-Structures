#Recorrido por amplitud
from Estructuras import Cola
from Grafo import Grafo

def bfs_amplitud(grafo: Grafo, inicio):
    espera = set()  # seguimiento de nodos procesados (aqui se irá viendo el orden del camino)
    cola = Cola()  # se usa una pila para la busqueda profunda inicializandola con el primer nodo(inicio)
    cola.encolar(inicio)
    recorridoAmplitud = { grafo.listaVertices[i]: [] for i in range(grafo.n) }
    espera.update(recorridoAmplitud.keys()) # colocar vertices en espera
    espera.difference_update(inicio) # eliminar de la lista de espera | marcar listo
    
    while not cola.esta_vacia():  # Continua hasta que la cola esta vacía
        nodo = cola.desencolar()  # saca el nodo de la cola y lo almacena para ser usado despues
        print(nodo)        # Imrpime el nodo actual (para visualizar)
        for vertice in grafo.vertices[nodo]: #recorrer lista de vertices adyacentes
            if vertice in espera:
                cola.encolar(vertice) # encolar vertice
                recorridoAmplitud[nodo].append(vertice) # representar  el recorrido
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

# DFS o busqueda profunda
        
# Llamamos a a funcion que creamos dando inicio en el nodo "A"

res = Grafo( diccionarioAdjacencia=bfs_amplitud(grafo, 'S'))
print("Representación | Grafo del arbol resultante :\n")
print(res)


