#Recorrido por amplitud
from Estructuras import Cola
import networkx as nx
def bfs_amplitud(G, inicio):
    espera = set()  # conjunto de vertices o nodos en espera
    cola = Cola()  # instancia de clase Cola
    cola.encolar(inicio) # encolar  (marcar como listo) al vertice inicial
    recorridoAmplitud = { G.listaVertices[i]: [] for i in range(G.n) } # diccionario de G resultante
    
    espera.update(recorridoAmplitud.keys()) # colocar vertices en espera
    espera.difference_update(inicio) # eliminar de la lista de espera | marcar listo
    
    while not cola.esta_vacia():  # Continua hasta que la cola esta vacía
        nodo = cola.desencolar()  # saca el nodo de la cola y lo almacena para ser usado despues
        print(nodo) # Imprime el nodo actual (para visualizar)
        for vertice in G.vertices[nodo]: #recorrer lista de vertices adyacentes al nodo
            if vertice in espera: # si el vertice actual esta en espera
                cola.encolar(vertice) # encolar vertice
                recorridoAmplitud[nodo].append(vertice) # añadir adyacentes en la lista del nodo
                espera.difference_update(vertice) # eliminar de la lista de espera | marcar listo
                
    return recorridoAmplitud

