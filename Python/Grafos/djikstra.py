import networkx as nx 
import matplotlib.pyplot as plt 

g=nx.DiGraph()#creamos el grafo

print("Defina los vertices del grafo DIRIGIDO\n")
while True:
    vertice = input("\nIntroduce un vertice\n-1 para salir : ")
    
    if vertice == "-1":
        print("\nSaliendo...")
        break
    
    if not vertice.isalnum():
        print("El vertice debe ser al menos un caracter o digito.")
        continue
    
    if vertice not in g.nodes: # si el  vertice  no esta repetido
        g.add_node(vertice) # añadir nodo
    else:
        print(f"El vertice '{vertice}' ya existe.")

for vertice in g.nodes:
    print(f"\nDefiniendo adyacencias para el vértice: '{vertice}'")
    print("\nVértices disponibles:", g.nodes)
    while True:
        adj = input(f"\nIngresa un vértice adyacente a '{vertice}' (-1 para terminar): ").strip()  # Eliminar espacios en blanc
        if adj == "-1":
            break  # Salir del bucle para este vértice
        
        if adj in g.nodes:  # Verificar si el vértice adyacente existe
            if not adj in g.adj[vertice]:  # Evitar duplicados
                
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
                g.add_edge(vertice,adj, weight=costo)
                print(f"'\n{adj}' agregado como adyacente a '{vertice}' con un costo de {costo}.")

            else:
                print(f"'{adj}' ya está en la lista de adyacencia de '{vertice}'.")
        else:
            print(f"Error: '{adj}' no es un vértice válido.")


# Dibujar el grafo
ax = plt.subplot(111)  # Tamaño de la figura
pos = nx.spring_layout(g)  # Posiciones de los nodos
nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)

# Dibujar los pesos en las aristas
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)


plt.show(block=False)#mostramos el grafo
input("...")


while True:
    #ingrese el incio y el destino
    inicio=input("Ingrese el nodo inicio: ")
    destino=input("Ingrese el nodo final: ")


    #calculamos el camino ma corto con el método nx.shortest_path()
    try:
        camino_mas_corto=nx.shortest_path(g,inicio,destino,weight="weight")#algoritmo djiskstra inlcuido en la biblioteca networkx
        print(f"\n Camino mas corto es: {camino_mas_corto}")
    except nx.NetworkXNoPath:
            print("no existe camino entre esos dos nodos")    
    except nx.NodeNotFound:
        print(f"nodo no encontrado")

    
            
    
        

