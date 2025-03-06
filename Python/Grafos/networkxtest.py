import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
G = nx.Graph(name="Grafo") # instancia de grafo no dirigido
G.add_node(1) # añade el nodo 1
G.add_nodes_from([2,3]) # añade lista de nodos
G.add_nodes_from([(4, {"color": "red"}), (5, {"color": "green"})]) # con atributos

# vertices
G.add_edge(1,2)
G.add_edge(1,2) #e pueden colocar repetidos
subax1 = plt.subplot(111)
G.add_edge(1,6) #se pueden colocar inexistentes
e = (2, 3)
G.add_edge(*e)  # desempacar tupla

print(G.nodes)
print(G.edges)
print(G.number_of_nodes(), G.number_of_edges())
print(G.adj[1]) # adjacentes del nodo 1 en el grafo
tuplas = [(n, nbrdict) for n, nbrdict in G.adjacency()]
print(tuplas) # lista de adjacencia

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()