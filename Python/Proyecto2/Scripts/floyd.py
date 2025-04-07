import numpy as np

def floyd_warshall(G):
    """
    Implementa el algoritmo de Floyd-Warshall para encontrar los caminos más cortos entre todos los pares de nodos.
    :param G: Grafo dirigido con pesos en las aristas.
    :return: Tupla con la matriz de costos (C) y la matriz de predecesores (P).
    """
    n = G.number_of_nodes()
    nodos = list(G.nodes)
    P = np.full((n, n), None)  # Matriz de predecesores
    C = np.full((n, n), np.inf)  # Matriz de costos

    # Inicializamos las matrices con los valores de las aristas del grafo
    for a, b in G.edges:
        i, j = nodos.index(a), nodos.index(b)
        C[i, j] = G[a][b]['weight']
        P[i, j] = i  # El predecesor de b es a

    np.fill_diagonal(C, 0)  # La diagonal debe ser cero, ya que el costo de ir de un nodo a sí mismo es cero

    # Algoritmo de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if C[i, k] + C[k, j] < C[i, j]:
                    temp = C[i, j]
                    C[i, j] = C[i, k] + C[k, j]
                    P[i, j] = P[k, j]
                    if temp != C[i, j]:
                        print("\nCosto Anterior:", temp)
                        print(f"{nodos[i]} -> {nodos[j]}: min( {temp}, {nodos[i]}->{nodos[k]}+{nodos[k]}->{nodos[j]} ) ={C[i, j]}")

    return C, P

def reconstruir_camino_floyd(G, C, P, origen, destino):
    """
    Reconstruye el camino más corto entre dos nodos usando la matriz de predecesores.
    :param G: Grafo dirigido con pesos en las aristas.
    :param C: Matriz de costos.
    :param P: Matriz de predecesores.
    :param origen: Nodo de origen.
    :param destino: Nodo de destino.
    :return: Lista de aristas que forman el camino más corto.
    """
    nodos = list(G.nodes)
    i, j = nodos.index(origen), nodos.index(destino)
    
    if C[i, j] == np.inf:
        return []  # No hay camino entre los nodos
    
    camino = []
    while j is not None and j != i:
        camino.append((nodos[P[i, j]], nodos[j]))  # Agregamos la arista (predecesor, destino)
        j = P[i, j]
    return list(reversed(camino))

def encontrar_rutas_contaminadas_reciclaje(G, contaminadas, reciclaje):
    """
    Encuentra las rutas más cortas entre las zonas contaminadas y las zonas de reciclaje.
    :param G: Grafo dirigido con pesos en las aristas.
    :param contaminadas: Conjunto de nodos de zonas contaminadas.
    :param reciclaje: Conjunto de nodos de zonas de reciclaje.
    :return: Lista de rutas más cortas entre zonas contaminadas y zonas de reciclaje.
    """
    # Ejecutamos Floyd-Warshall para encontrar los caminos más cortos
    C, P = floyd_warshall(G)
    
    rutas = []
    for origen in contaminadas:
        for destino in reciclaje:
            ruta = reconstruir_camino_floyd(G, C, P, origen, destino)
            if ruta:
                rutas.append((origen, destino, ruta, C[list(G.nodes).index(origen), list(G.nodes).index(destino)]))  # (origen, destino, ruta, costo)
    
    return rutas
