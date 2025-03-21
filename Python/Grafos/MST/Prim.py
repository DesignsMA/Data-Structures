import networkx as nx
import matplotlib.pyplot as plt

# Paso 1: Crear el grafo
g = nx.Graph()

n_aristas = int(input("Ingrese el número de aristas del grafo: "))

# Creación de nodos y aristas para construir el grafo
for _ in range(n_aristas):
    nodo1 = input("Ingrese la etiqueta del nodo 1: ")
    nodo2 = input("Ingrese la etiqueta del nodo 2: ")
    peso = float(input("Ingrese el peso del camino/arista: "))
    g.add_edge(nodo1, nodo2, weight=peso)

# Mostrar el grafo
print("\nEl grafo construido es:")
print("Nodos:", g.nodes)
print("Aristas con peso:", g.edges(data=True))

# Paso 2: Inicializar variables
start = input("\nIngrese el nodo de inicio: ")

# Verificar que el nodo inicial está en el grafo
if start not in g.nodes:
    print("Error: El nodo de inicio no existe en el grafo.")
    exit()

U = {start}  # Aseguramos que U inicie con 'start'
Tree = []  # Lista de aristas del MST
sumatoria_pesos = 0

try:
    # Paso 3: Algoritmo de Prim
    while len(U) < len(g.nodes):
        aristas_candidatas = []

        for nodo in U:
            if nodo not in g:
                print(f"Error: El nodo {nodo} no está en el grafo.")
                exit()

            for vecino, atributos in g[nodo].items():  # Forma más segura que g.adjacency()
                if vecino not in U:
                    if "weight" not in atributos:
                        print(f"Error: La arista {nodo}-{vecino} no tiene peso.")
                        exit()
                    aristas_candidatas.append((nodo, vecino, atributos["weight"]))

        if not aristas_candidatas:
            raise nx.NetworkXNoPath  # Si no hay aristas disponibles, el grafo no es conexo

        # Seleccionar la arista de menor peso
        arista_min = min(aristas_candidatas, key=lambda x: x[2])

        # Agregar la arista al árbol de expansión mínima
        nodo1, nodo2, peso = arista_min
        print(f"Agregando arista: {nodo1}-{nodo2} con peso {peso}")  # Depuración
        U.add(nodo2)
        Tree.append((nodo1, nodo2, peso))
        sumatoria_pesos += peso

except nx.NetworkXNoPath:
    print("No existe un camino que conecte todos los nodos.")
    exit()
except KeyError:
    print("Error: Nodo no encontrado.")
    exit()

# Paso 4: Mostrar resultados
print("\nEl Árbol de Expansión Mínima (MST) es:")
print(Tree)
print(f"La sumatoria total de los pesos es: {sumatoria_pesos}")














# Visualización

# Grafo original
pos = nx.spring_layout(g)  # Posiciones para los nodos
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
nx.draw(g, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_size=12)
labels = nx.get_edge_attributes(g, "weight")
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
plt.title("Grafo Original")

# Crear el grafo MST
mst_graph = nx.Graph()
mst_graph.add_weighted_edges_from(Tree)

plt.subplot(1, 2, 2)
nx.draw(mst_graph, pos, with_labels=True, node_color="lightgreen", edge_color="red", node_size=2000, font_size=12)
labels_mst = {(u, v): w for u, v, w in Tree}  # Etiquetas de peso corregidas
nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=labels_mst)
plt.title("Árbol de Expansión Mínima (MST)")

plt.show()