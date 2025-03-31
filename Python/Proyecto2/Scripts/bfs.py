import networkx as nx

def bfs_amplitud(grafo: nx.Graph, inicio):
    """
    Implementación de BFS que devuelve un nuevo grafo con la estructura del recorrido en amplitud.
    
    Args:
        grafo (nx.Graph): Grafo original de NetworkX
        inicio: Nodo de inicio del recorrido
        
    Returns:
        nx.Graph: Nuevo grafo que representa el árbol BFS
    """
    # Crear nuevo grafo dirigido para el árbol BFS
    arbol_bfs = nx.DiGraph()
    
    # Estructuras para el recorrido
    visitados = set()
    cola = [inicio]
    visitados.add(inicio)
    
    while cola:
        nodo_actual = cola.pop(0)
        
        # Explorar vecinos
        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                # Añadir al árbol BFS
                arbol_bfs.add_edge(nodo_actual, vecino)
                
                # Marcar como visitado y encolar
                visitados.add(vecino)
                cola.append(vecino)
    
    return arbol_bfs

def encontrar_mas_cercano_con_ruta(arbol_bfs: nx.DiGraph, inicio, filtro: list):
    """
    Encuentra el nodo más cercano al inicio en el árbol BFS y la ruta que los conecta.
    
    Args:
        arbol_bfs (nx.DiGraph): Árbol BFS (resultado de bfs_amplitud)
        inicio: Nodo de inicio
        filtro (list): Lista de filtro
        
    Returns:
        tuple: (distancia, nodo_mas_cercano, lista_de_aristas)
        Si no se encuentra, retorna (-1, None, [])
    """
    from collections import deque
    
    # Estructuras para BFS
    cola = deque([(inicio, 0, [])])  # (nodo_actual, distancia, ruta)
    visitados = set([inicio])
    
    while cola:
        nodo_actual, distancia, ruta = cola.popleft()
        
        # Verificar si cumple el criterio (excepto el nodo inicial)
        if nodo_actual != inicio:
            if nodo_actual in filtro: # si el nodo esta en la lista de contaminadas o filtro
                return (distancia, nodo_actual, ruta)
        
        # Explorar vecinos
        for vecino in arbol_bfs.successors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                nueva_ruta = ruta + [(nodo_actual, vecino)]
                cola.append((vecino, distancia + 1, nueva_ruta))
    
    return (-1, None, []) # no encontrado