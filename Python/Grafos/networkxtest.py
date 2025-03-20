import networkx as nx
import numpy as np
import matplotlib.pyplot as plt # usado para graficar los nodos
G = nx.DiGraph(name="Grafo") # instancia de grafo no dirigido
G.add_nodes_from(['2',3]) # añade lista de nodos
G.add_nodes_from([(4, {"color": "red"}), (5, {"color": "green"})]) # con atributos

# vertices
G.add_edge(1,'2', weight=9)
G.add_edge(1,4, weight=1)
G.add_edge(1,4, weight=3)
G.add_edge(1,4, weight=5)
G.add_edge(5,1, weight=4)
e = ('2', 3)
G.add_edge(*e,weight=9)  # desempacar tupla


print(G.nodes)
print(G.edges)
for a,b in G.edges:
    print(a,b)
print(G.number_of_nodes(), G.number_of_edges())
print(sorted( G.edges(data=True), key=lambda x: x[2]['weight']))
n = G.number_of_nodes()
C = np.full((n,n), np.inf)
V = list(G.nodes)
for a,b in G.edges: # por cada par de vertices que definen a un arista
    C[V.index(a), V.index(b)] = G.adj[a][b]['weight'] # en la posición correspondiente a la matriz, asignar el peso de ir de a a b           
print(C)
tuplas = [(n, nbrdict) for n, nbrdict in G.adjacency()]
print(tuplas) # lista de adjacencia
print(nx.attr_matrix(G, edge_attr="weight", rc_order=G.nodes))
H = nx.DiGraph(G) #digrafo
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122) #subplot, (ncols, nrows, index)
nx.draw(H, with_labels=True, font_weight='bold')
plt.show()