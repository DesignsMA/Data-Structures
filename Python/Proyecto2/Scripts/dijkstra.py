import numpy as np

def reconstruirCaminos(G, origen, predecesores: dict):
    """
    Reconstruye todos los caminos más cortos desde un nodo origen usando los predecesores.
    
    :param origen: Nodo de origen.
    :param predecesores: Diccionario de predecesores (nodo -> nodo predecesor).
    :return: Diccionario de caminos más cortos (nodo -> lista de aristas).
    """
    caminos = {}
    for nodo in predecesores:
        camino = []
        actual = nodo
        while actual != origen and actual in predecesores:
            anterior = predecesores[actual]
            camino.insert(0, (anterior, actual))  # Insertamos al principio para mantener orden
            actual = anterior
        caminos[nodo] = camino
    return caminos

def dijkstraFunc(G, origen, destino: str = 'todo'):
    """
    Implementa el algoritmo de Dijkstra para encontrar los caminos más cortos desde un nodo origen.
    
    :param G: Grafo (NetworkX Graph o DiGraph)
    :param origen: Nodo de origen
    :param destino: 'todo' para todos los destinos, o nodo específico
    :return: Depende del destino:
             - Si 'todo': (distancias, predecesores, caminos)
             - Si nodo específico: (distancia, predecesor, camino)
    """
    n = G.number_of_nodes()
    V = list(G.nodes)
    
    # Inicialización
    D = {v: np.inf for v in V}  # Distancias
    D[origen] = 0
    P = {v: None for v in V}    # Predecesores
    S = set()                   # Nodos visitados

    C = np.full((n, n), np.inf)
    for a, b in G.edges:
        C[V.index(a), V.index(b)] = G.adj[a][b]['weight']
    
    # Algoritmo principal
    for _ in range(n):
        # Encontrar nodo no visitado con menor distancia
        nodos_no_visitados = [v for v in V if v not in S]
        if not nodos_no_visitados:
            break
            
        u = min(nodos_no_visitados, key=lambda v: D[v])
        
        S.add(u)
        
        # Actualizar distancias de vecinos
        for v in G.neighbors(u):
            if v not in S:
                distancia_alternativa = D[u] + C[V.index(u), V.index(v)]
                if distancia_alternativa < D[v]:
                    D[v] = distancia_alternativa
                    P[v] = u
    
    # Reconstruir caminos
    todos_los_caminos = reconstruirCaminos(G, origen, P)
    
    if destino == 'todo':
        return D, P, todos_los_caminos
    else:
        if destino not in D:
            return np.inf, None, []
        return D[destino], P[destino], todos_los_caminos[destino]