import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
G = nx.DiGraph(name="Grafo") # instancia de grafo no dirigido
G.add_nodes_from([2,3]) # añade lista de nodos
G.add_nodes_from([(4, {"color": "red"}), (5, {"color": "green"})]) # con atributos

# vertices
G.add_edge(1,2, weight=9)
e = (2, 3)
G.add_edge(*e,weight=9)  # desempacar tupla


print(G.nodes)
print(G.edges)
print(G.number_of_nodes(), G.number_of_edges())
print(G.adj[1]) # adjacentes del nodo 1 en el grafo
tuplas = [(n, nbrdict) for n, nbrdict in G.adjacency()]
print(tuplas) # lista de adjacencia
print(nx.attr_matrix(G, edge_attr="weight", rc_order=G.nodes))
H = nx.DiGraph(G) #digrafo
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122) #subplot, (ncols, nrows, index)
nx.draw(H, with_labels=True, font_weight='bold')
plt.show()