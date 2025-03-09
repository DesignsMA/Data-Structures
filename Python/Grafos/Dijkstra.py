import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
import numpy as np
G = nx.DiGraph() # instanciando grafo DIRIGIDO

def dijkstra(G: nx.DiGraph, origen):
    # Número de nodos
        n = G.number_of_nodes()

        # Lista de nodos para mapear índices
        V = list(G.nodes)

        # Matriz de costos
        C = np.full((n,n), np.inf)
        for a,b in G.edges: # por cada par de vertices que definen a un arista
            C            
            
        print("Matriz de costos:\n", C)

        # Inicialización de S, D y P
        S = set([origen])  # S inicia con el origen (usando un conjunto)
        D = {}  # Diccionario de distancias
        P = {}  # Diccionario de predecesores

        # Inicializando distancias
        for i in range(n):
            if V[i] == origen:  # El nodo de origen tiene distancia 0
                D[V[i]] = 0
            else:
                if (origen, V[i]) in G.edges:  # Si hay conexión
                    D[V[i]] = C[V.index(origen), i]
                else:  # Si no hay conexión
                    D[V[i]] = np.inf

        # Bucle principal
        for _ in range(n-1):
            # Elige un vértice w en V-S tal que D[w] es mínimo
            w = min((v for v in V if v not in S), key=lambda v: D[v])

            # Agrega w a S
            S.add(w)

            # Actualiza las distancias de los vecinos de w
            for v in V:
                if v not in S and C[V.index(w), V.index(v)] != np.inf:
                    if D[w] + C[V.index(w), V.index(v)] < D[v]:
                        P[v] = w  # Añadir predecesor si pasando por w, mejora camino
                        D[v] = D[w] + C[V.index(w), V.index(v)]
        return D, P        
            
                
print("Defina los vertices del grafo DIRIGIDO\n")
while True:
    vertice = input("\nIntroduce un vertice\n-1 para salir : ")
    
    if vertice == "-1":
        print("\nSaliendo...")
        break
    
    if not vertice.isalnum():
        print("El vertice debe ser al menos un caracter o digito.")
        continue
    
    if vertice not in G.nodes: # si el  vertice  no esta repetido
        G.add_node(str(vertice)) # añadir nodo
    else:
        print(f"El vertice '{vertice}' ya existe.")

for vertice in G.nodes:
    print(f"\nDefiniendo adyacencias para el vértice: '{vertice}'")
    print("\nVértices disponibles:", G.nodes)
    while True:
        adj = input(f"\nIngresa un vértice adyacente a '{vertice}' (-1 para terminar): ").strip()  # Eliminar espacios en blanc
        if adj == "-1":
            break  # Salir del bucle para este vértice
        
        if adj in G.nodes:  # Verificar si el vértice adyacente existe
            if not adj in G.adj[vertice]:  # Evitar duplicados
                
                while True:
                    try:
                        costo = input(f"\nDefine el costo del recorrido hacia {adj} | Solo positivos: ")
                        costo = float(costo)
                        if costo < 0:
                            print("Solo se puede tener un costo mayor a cero.")
                            continue # repetir
                    except ValueError as e:
                        print("No es un número real positivo.")
                        continue
                    
                    break
                
                arista = (vertice,adj,costo)
                G.add_edge(vertice,adj, weight=costo)
                print(f"\n'{adj}'agregado como adyacente a '{vertice}' con un costo de {costo}.")

            else:
                print(f"'{adj}' ya está en la lista de adyacencia de '{vertice}'.")
        else:
            print(f"Error: '{adj}' no es un vértice válido.")

ax = plt.subplot(111)
pos = nx.spring_layout(G, seed=7)  # posicion de los nodos
# nodos
nx.draw_networkx_nodes(G,pos, node_size=200, node_color='#ff5353')
# aristas
nx.draw_networkx_edges(G,pos, width=2)

# etiquetas de nodos
nx.draw_networkx_labels(G, pos,font_size=10, font_family="Montserrat", font_color='white', font_weight='bold')
# etiquetas con peso de aristas
edge_labels = nx.get_edge_attributes(G, "weight") # retorna diccionario de atributos
nx.draw_networkx_edge_labels(G,pos, edge_labels,font_size=10, font_color='#ff5353',font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec":(1.0, 1.0, 1.0),"fc":(1.0, 1.0, 1.0), "alpha": 0.6}) # por cada arista colocar etiqueta

print("Visualize su grafo a continuación: ")

plt.show(block=False)
while True:
    print("\nNodos disponibles: ", list(G.nodes))
    origen = input("\nIntroduzca su nodo origen, escriba 'Salir' para salir: ")
    if origen == 'Salir':
        break
    
    try:
        G.nodes[origen]
        Distancias, Predecesores = dijkstra(G, origen)
        print(f"\nDistancias mas cortas de {origen} a los demas nodos: ")
        for nodo, distancia in Distancias.items():
            print(f"{origen} -> {nodo}: {distancia}")
        print(Predecesores)
        #print(f"\nDistancias mas cortas de {origen} a los demas nodos: ")
        #for nodo, distancia in Distancias.items():
        #    print(f"{origen} -> {nodo}: {distancia}")
    except KeyError as e:
        print("El nodo no existe.")
    except EOFError:
        print("Error, fin de archivo.")

input("Terminar programa...")