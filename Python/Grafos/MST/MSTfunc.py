import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def kruskal(G: nx.Graph):
    
    if not G.is_directed() and nx.is_connected(G): # si el grafo es conexo y no dirigido
        V = set( G.nodes ) # conjunto de vertices
        # Estructura para manejar las componentes conexas (Union-Find)
        C = {}  # Diccionario para almacenar el padre de cada vértice

        def INICIAL(v):
            """Inicializa una componente conexa para el vértice v."""
            C[v] = v  # Cada vértice es su propio padre inicialmente

        def ENCUENTRA(v):
            """Encuentra la componente conexa a la que pertenece el vértice v."""
            if C[v] != v:
                C[v] = ENCUENTRA(C[v])  # Compresión de camino
            return C[v]

        def COMBINA(u, v):
            """Combina las componentes conexas de u y v."""
            root_u = ENCUENTRA(u)
            root_v = ENCUENTRA(v)
            if root_u != root_v:
                C[root_v] = root_u  # Une las componentes
        
        comp_sig = 0
        for v in V:
            comp_sig +=1
            INICIAL(v) # cada vertice es componente de si mismo
        
        # Lista ordenada de la lista de tuplas (a,b,{weight: int}) usando como campo de comparacion su campo x[2]['weight'] 
        A = sorted( G.edges(data=True), key=lambda x: x[2]['weight'])
        MST = nx.Graph() # instancia del grafo del arbol

        for a in A: # va de menor peso a mayor
            u,v,weight = a
            # determina a que componente pertenece cada vértice
            if ENCUENTRA(u) != ENCUENTRA(v):  # Si no forman un ciclo
                MST.add_edge(u, v, **weight)  # Añadir la arista al MST
                COMBINA(u, v)  # Combinar las componentes

        return MST
    else:
        raise ValueError("El grafo debe ser no dirigido y conexo.")

        


# Ejemplo de uso
G = nx.Graph()
G.add_edges_from([
    ('A', 'B', {'weight': 1}),
    ('B', 'C', {'weight': 2}),
    ('C', 'D', {'weight': 3}),
    ('D', 'A', {'weight': 4}),
    ('A', 'C', {'weight': 5})
])

MST = kruskal(G)
