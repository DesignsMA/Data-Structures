import networkx as nx

def dfs_profundidad(grafo, inicio):
    visitados = set()
    recorrido_aristas = []
    pila = [(inicio, None)]  # Guardamos (nodo_actual, nodo_padre)

    while pila:
        nodo, padre = pila.pop()
        if nodo not in visitados:
            visitados.add(nodo)
            if padre is not None:  # Evita agregar arista para el nodo inicial
                peso = grafo.get_edge_data(padre, nodo).get('weight', None)
                recorrido_aristas.append((padre, nodo, peso))
            # Agregamos vecinos en orden inverso para procesarlos en orden original
            for vecino in reversed(list(grafo.neighbors(nodo))):
                if vecino not in visitados:
                    pila.append((vecino, nodo))

    return recorrido_aristas

def encontrar_mas_lejano_con_ruta(arbol: nx.DiGraph, origen, filtro: list):
    """
    Encuentra el nodo más alejado en el árbol a partir de un nodo de origen
    que también pertenezca al filtro de nodos, junto con la distancia y la ruta que conecta ambos,
    representada como una lista de aristas (tuplas de nodos consecutivos).
    
    Args:
        arbol (nx.DiGraph): Árbol representado como un grafo dirigido.
        origen: Nodo de origen
        filtro (set): Conjunto de nodos a filtrar (solo los nodos en este conjunto se considerarán).
    
    Returns:
        tuple: (distancia, nodo_mas_alejado, ruta_en_aristas)
        Si no se encuentra, retorna (-1, None, [])
    """
    # Obtener las rutas más cortas desde el nodo de origen usando NetworkX
    rutas = nx.single_source_shortest_path(arbol, origen)
    
    # Filtrar solo los nodos que estén en el filtro
    nodos_filtrados = {nodo: ruta for nodo, ruta in rutas.items() if nodo in filtro}
    
    if not nodos_filtrados:
        return (-1, None, [])  # Si no hay nodos en el filtro
    
    # Encontrar el nodo más alejado dentro de los nodos filtrados
    nodo_mas_alejado = max(nodos_filtrados, key=lambda x: len(nodos_filtrados[x]))
    ruta_mas_alejada = nodos_filtrados[nodo_mas_alejado]
    
    # Convertir la ruta de nodos a una lista de aristas
    ruta_en_aristas = [(ruta_mas_alejada[i], ruta_mas_alejada[i+1]) for i in range(len(ruta_mas_alejada)-1)]
    
    distancia_maxima = len(ruta_mas_alejada) - 1  # La distancia es la longitud de la ruta menos 1
    
    return distancia_maxima, nodo_mas_alejado, ruta_en_aristas
