import networkx as nx

def dfs_profundidad(G, inicio):
    verificado = set()  # Seguimiento de nodos visitados
    pila = [inicio]  # Se usa una pila para la búsqueda en profundidad
    recorrido_aristas = []  # Lista para almacenar las aristas recorridas

    while pila:  # Mientras la pila no esté vacía
        nodo = pila.pop()  # Extrae el nodo de la pila
        if nodo not in verificado:
            verificado.add(nodo)  # Marca el nodo como visitado
            for vecino in reversed(list(G.neighbors(nodo))):  # Recorre los vecinos en orden inverso
                if vecino not in verificado:
                    recorrido_aristas.append((nodo, vecino))  # Agrega la arista al recorrido
                    pila.append(vecino)  # Agrega el vecino a la pila

    return recorrido_aristas  # Retorna la lista de aristas recorridas