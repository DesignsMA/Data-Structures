import numpy as np
def reconstruirCaminoDijkstra(G, origen, predecesores: dict, destino: str = None):
    """
    Reconstruye el camino más corto desde el nodo origen hasta el destino usando los predecesores.
    :param origen: Nodo de origen.
    :param predecesores: Diccionario de predecesores.
    :param destino: Nodo de destino (opcional). Si no se especifica, se reconstruyen todos los caminos.
    :return: Lista de caminos más cortos.
    """
    # Si no se proporciona un destino, reconstruir todos los caminos
    if destino is None:
        destinos = G.nodes
    else:
        destinos = [destino]
    
    aristas = []
    for nodo in destinos:
        camino = []
        actual = nodo
        while actual != origen:
            if actual in predecesores:
                anterior = predecesores[actual]
                arista = (anterior, actual)
                camino.insert(0, arista)  # Insertar al principio para tener el orden correcto
                actual = anterior
            else:
                # Si no hay predecesor, significa que no hay camino
                camino = []
                break
        if camino:
            aristas.append(camino)
    return aristas

def dijkstraFunc(G, origen, destino: str = 'todo'):
    """
    Implementa el algoritmo de Dijkstra para encontrar los caminos más cortos desde un nodo origen.
    :param origen: Nodo desde el cual se calcularán los caminos más cortos.
    :return: Tupla con las distancias más cortas, los predecesores de cada nodo, lista de aristas del camino.
    """
    n = G.number_of_nodes()
    V = list(G.nodes)
    # Matriz de costos
    C = np.full((n, n), np.inf)
    for a, b in G.edges:
        C[V.index(a), V.index(b)] = G.adj[a][b]['weight']
    print("Matriz de costos:\n", C)
    # Inicialización de S, D y P
    S = set([origen])
    D = {}  # Diccionario de distancias
    P = {}  # Diccionario de predecesores
    # Inicializando distancias
    for i in range(n):
        if V[i] == origen:
            D[V[i]] = 0
        else:
            if (origen, V[i]) in G.edges:
                D[V[i]] = C[V.index(origen), i]
            else:
                D[V[i]] = np.inf
    # Bucle principal
    Predecesores = {v: {} for v in V}
    for _ in range(n - 1):
        P = {}  # Reiniciando P
        w = min((v for v in V if v not in S), key=lambda v: D[v])
        S.add(w)
        # Actualiza las distancias de los vecinos de w
        for v in V:
            if v not in S and C[V.index(w), V.index(v)] != np.inf:
                if D[w] + C[V.index(w), V.index(v)] < D[v]:
                    P[v] = w
                    D[v] = D[w] + C[V.index(w), V.index(v)]
                    Predecesores[V[V.index(v)]] = P
    if destino == 'todo':
        return D, Predecesores, reconstruirCaminoDijkstra(G,origen,Predecesores)
    else:
        return D[destino], Predecesores[destino], reconstruirCaminoDijkstra(G,origen,Predecesores,destino)
