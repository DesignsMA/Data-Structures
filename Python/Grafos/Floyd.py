import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
import numpy as np
G = nx.DiGraph() # instanciando grafo DIRIGIDO
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
        G.add_node(vertice) # añadir nodo
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
                print(f"'\n{adj}' agregado como adyacente a '{vertice}' con un costo de {costo}.")

            else:
                print(f"'{adj}' ya está en la lista de adyacencia de '{vertice}'.")
        else:
            print(f"Error: '{adj}' no es un vértice válido.")

fig = plt.figure(figsize=(12, 8))  # Ajusta el tamaño de la figura a toda la ventana
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Elimina los márgenes
pos = nx.spring_layout(G, seed=728, k=3/np.sqrt(G.number_of_nodes())) # posicion de los nodos
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
n = G.number_of_nodes()

# Algoritmo de floyd-warshall
print("Número de nodos:", n)

# Crear matriz de adyacencia inicializada con infinitos
nodos = list(G.nodes)  # Lista de nodos para mapear índices
C = np.full((n,n), np.inf)
for a,b in G.edges: # por cada par de vertices que definen a un arista
    C[nodos.index(a), nodos.index(b)] = G.adj[a][b]['weight'] # en la posición correspondiente a la matriz, asignar el peso de ir de a a b           
# Establecer la diagonal principal en 0
np.fill_diagonal(C, 0)

print("Matriz de adyacencia inicial (C):")
print(C)
A = np.copy(C)

nodos = list(G.nodes)
for k in range(n): # nodo intermedio
    for i in range(n): # nodo origen
        for j in range(n): # nodo destino
            if A[i,k] + A[k,j] < A[i,j]: # pasar por k reduce
                temp = A[i,j]
                A[i,j] = A[i,k] + A[k,j] # actualizar el costo actual
                
                if temp != A[i,j]: # si hubo un cambio
                    print("\nCosto Anterior: ", temp)
                    print(f"{nodos[i]} -> {nodos[j]}: min( {temp}, {nodos[i]}->{nodos[k]}+{nodos[k]}->{nodos[j]} ) ={A[i,j]}")

print("\nMatriz de costos final (A):\n", A)

input("Terminar programa...")