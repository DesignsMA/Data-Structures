import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos

g=nx.Graph()#creamos el grafo

n_aristas=int(input("Ingrese el numero de aristas del grafo:"))#la base del programa es saber las aristas del grafo

#creacion de nodos y aristas
for _ in range(n_aristas):
    nodo1=input("Ingrese la etiqueta del nodo: ")
    nodo2=input("Ingrese la etiqueta del nodo: ")
    peso=float(input("Ingrese el peso del camino/arista"))
    g.add_edge(nodo1,nodo2,weight=peso)

    
#mostramos el grafo    
print("El grafo construido es: ")
print(g.nodes)
print("Pesos de las aristas: ", g.edges(data=True))    


# Dibujar el grafo
ax = plt.subplot(111)  # Tamaño de la figura
pos = nx.spring_layout(g)  # Posiciones de los nodos
nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)

# Dibujar los pesos en las aristas
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)


plt.show(block=False)#mostramos el grafo
input("...")


#ingrese el incio y el destino
inicio=input("ingrese el nodo inicio: ")
destino=input("ingrese el nodo final: ")


#calculamos el camino ma corto con el método nx.shortest_path()
try:
    camino_mas_corto=nx.shortest_path(g,inicio,destino,weight="weight")#algoritmo djiskstra inlcuido en la biblioteca networkx
    print(f"\n Camino mas corto es: {camino_mas_corto}")
except nx.NetworkXNoPath:
        print("no existe camino entre esos dos nodos")    
except nx.NodeNotFound:
    print(f"nodo no encontrado")