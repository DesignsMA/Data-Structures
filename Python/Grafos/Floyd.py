import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
import numpy as np

# Función para reconstruir el camino mínimo
def reconstruirCamino(C, P, origen, destino):
    i, j = nodos.index(origen), nodos.index(destino)
    if C[i, j] == np.inf:  # No hay camino
        return []
    
    camino = []
    while j is not None and j != i:
        camino.append((nodos[P[i, j]], nodos[j]))
        j = P[i, j]
    
    return list(reversed(camino))

def redibujar(G: nx.DiGraph, pos, camino):
    nx.draw_networkx_nodes(G,pos, node_size=200, node_color='#ff5353')
    # etiquetas de nodos
    nx.draw_networkx_labels(G, pos,font_size=10, font_family="Montserrat", font_color='white', font_weight='bold')
    edges_diff = set(G.edges) - set(camino)
    edge_labels_diff = {edge: G[edge[0]][edge[1]]["weight"] for edge in edges_diff}  # Aristas NO usadas
    edge_labels = {edge: G[edge[0]][edge[1]]["weight"] for edge in camino if edge in G.edges}
    # aristas no usados
    nx.draw_networkx_edges(G,pos, edgelist=edges_diff,  width=2)
    nx.draw_networkx_edge_labels(G,pos, edge_labels_diff, font_size=10, font_color='#ff5353',font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec":(1.0, 1.0, 1.0),"fc":(1.0, 1.0, 1.0), "alpha": 0.6}) # por cada arista colocar etiqueta
    # aristas de caminos más cortos
    nx.draw_networkx_edges(G, pos, edgelist=camino, edge_color='#ff5353', width=2)
    nx.draw_networkx_edge_labels(G,pos, edge_labels,font_size=10, font_color='#040404',font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec":(1.0, 1.0, 1.0),"fc":(1.0, 1.0, 1.0), "alpha": 0.6}) # por cada arista colocar etiqueta



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

n = G.number_of_nodes()
fig = plt.figure(figsize=(12, 8))  # Ajusta el tamaño de la figura a toda la ventana
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Elimina los márgenes
pos = nx.spring_layout(G, seed=728, k=3/np.sqrt(n)) # posicion de los nodos

print("Visualize su grafo a continuación: ")

redibujar(G,pos,[]) # dibujo inicial
plt.show(block=False)

# Crear matriz de adyacencia inicializada con infinitos
nodos = list(G.nodes)  # Lista de nodos para mapear índices
P = np.full((n, n), None)  # Matriz de predecesores
C = np.full((n,n), np.inf)

for a,b in G.edges: # por cada par de vertices que definen a un arista
    i, j = nodos.index(a), nodos.index(b)
    C[i, j] = G[a][b]['weight']
    P[i, j] = i  # Predecesor de j es i
# Establecer la diagonal principal en 0

np.fill_diagonal(C, 0)
nodos = list(G.nodes)
# Algoritmo floyd-marshall
for k in range(n): # nodo intermedio
    for i in range(n): # nodo origen
        for j in range(n): # nodo destino
            if C[i,k] + C[k,j] < C[i,j]: # pasar por k reduce
                temp = C[i,j]
                C[i,j] = C[i,k] + C[k,j] # actualizar el costo actual
                P[i,j] = P[k,j] # Actualizar predecesor
                if temp != C[i,j]: # si hubo un cambio
                    print("\nCosto Anterior: ", temp)
                    print(f"{nodos[i]} -> {nodos[j]}: min( {temp}, {nodos[i]}->{nodos[k]}+{nodos[k]}->{nodos[j]} ) ={C[i,j]}")


while True:
    print("\nNodos disponibles: ", list(G.nodes))
    origen = input("\nIntroduzca su nodo origen, escriba 'Salir' para salir: ")
    if origen == 'Salir':
        break
    
    destino = input("\nIntroduzca su nodo destino, escriba 'todo' para resaltar todos los caminos: ")

    
    try:
        G.nodes[origen] # comprobar existencia
        if destino != 'todo':
            G.nodes[destino]
                    
        print(f"\nDistancias mas cortas de {origen} a los demas nodos: ")
        for j in range( len(C[nodos.index(origen)]) ):
            print(f"{origen} -> {nodos[j]}: {C[nodos.index(origen), j]}")
                    
        print(f"\nCaminos mas cortos de {origen} a los demas nodos: ")
        caminos = []
        for dest in nodos:
            camino = reconstruirCamino(C, P, origen, dest)
            print(f"{origen} -> {dest}: {camino}")     
            caminos.append(camino) # arreglo de camino
        
        print("\nVisualize los caminos más cortos\nMueva la figura para actualizar la vista.")
        
        fig.clear() # redibujar
        if destino == 'todo':
            todo = []
            for cam in caminos:
                todo += cam
            print(todo)
            redibujar(G,pos,todo)
        else:
            redibujar(G,pos,caminos[nodos.index(destino)]) # solo redibujar el camino destino

    except KeyError as e:
        print(f"El nodo de destino u origen no existe.\n")
    except EOFError:
        print("Error, fin de archivo.")
