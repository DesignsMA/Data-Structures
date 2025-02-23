#Recorrido por amplitud

from Grafo import Grafo
# Definimos el grafo mediante un diccionario de phyton
grafo = Grafo( dictionarioAdjacencia= {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': [],
    'D': ['F'],
    'E': [],
    'F': [],
})

# DFS o busqueda profunda
def dfs_profundidad(grafo, inicio):
    verificado = set()  # seguimiento de nodos verificados (aqui se irá viendo el orden del camino)
    pila = [inicio]  # se usa una pila para la busqueda profunda inicializandola con el primer nodo(inicio)
    l=[]

    while pila:  # Continua hasta que la pila esta vacía
        nodo = pila.pop()  # saca el nodo de la pila y lo almacena para ser usado despues
        if nodo not in verificado:
            verificado.add(nodo)  # Verifica el nodo añadiendolo al set para llevar el orden del camino
            l.append(nodo)
            print(nodo)        # Imrpime el nodo actual (para visualizar)
            pila.extend(reversed(grafo.vertices[nodo]))  # Añade nodos hijos a la pila en orden reverso 
    print(l)        
            
            
           




# Llamamos a a funcion que creamos dando inicio en el nodo "A"
dfs_profundidad(grafo, 'A')


