import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GrafoInteractivo:
    """
    Clase que representa una interfaz gráfica interactiva para manipular y visualizar grafos.
    Permite agregar vértices, aristas, calcular caminos más cortos usando Dijkstra y Floyd-Warshall,
    y visualizar los resultados en un gráfico.
    """

    def __init__(self, root: tk.Tk):
        """
        Inicializa la interfaz gráfica y configura el grafo interactivo.

        :param root: Ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("Grafo Interactivo con Menú")
        self.root.attributes('-topmost', True)  # Mantener en primer plano
        self.root.focus_force()  # Forzar el foco en la ventana

        # Crear el contenedor para el menú
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Botones del menú
        tk.Button(self.menu_frame, text="Agregar Vértice", command=self.agregar_vertice).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Agregar Arista", command=self.agregar_arista).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Dijkstra", command=self.dijkstra).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Floyd Warshall", command=self.floyd).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Siguiente camino | Floyd", command=self.siguienteCamino).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Limpiar resaltado", command=self.reset).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Salir", command=root.quit).pack(fill=tk.X, pady=20)

        # Crear la figura y el lienzo de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Elimina los márgenes

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Inicializar el grafo
        self.G = nx.DiGraph()
        self.pos = {}  # Posiciones de los nodos
        self.camino = []  # Camino actual resaltado
        self.caminos = []  # Lista de caminos calculados

        # Habilitar movimiento de nodos
        self.dragging = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def agregar_vertice(self):
        """
        Agrega un vértice al grafo. Solicita al usuario el nombre del vértice.
        """
        nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:", parent=self.root)
        if nombre and nombre not in self.G.nodes:
            self.G.add_node(nombre)
            self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
            self.dibujar_grafo()

    def agregar_arista(self):
        """
        Agrega una arista al grafo. Solicita al usuario el nodo origen, nodo destino y peso de la arista.
        """
        origen = simpledialog.askstring("Agregar Arista", "Ingrese el nodo origen:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        destino = simpledialog.askstring("Agregar Arista", "Ingrese el nodo destino:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        peso = simpledialog.askfloat("Agregar Arista", "Ingrese el peso de la arista:", parent=self.root)

        if origen in self.G.nodes and destino in self.G.nodes and peso:
            if peso >= 0:
                self.G.add_edge(origen, destino, weight=peso)
                self.dibujar_grafo()
            else:
                messagebox.showerror("Error", "El peso debe ser válido (0-Inf).")
        else:
            messagebox.showerror("Error", "Los nodos deben existir y el peso debe ser válido (0-Inf).")

    def reset(self):
        """
        Limpia el resaltado de los caminos y redibuja el grafo.
        """
        self.ax.clear()
        self.camino = []
        self.dibujar_grafo()

    def dijkstraFunc(self, origen):
        """
        Implementa el algoritmo de Dijkstra para encontrar los caminos más cortos desde un nodo origen.

        :param origen: Nodo desde el cual se calcularán los caminos más cortos.
        :return: Tupla con las distancias más cortas y los predecesores de cada nodo.
        """
        n = self.G.number_of_nodes()
        V = list(self.G.nodes)

        # Matriz de costos
        C = np.full((n, n), np.inf)
        for a, b in self.G.edges:
            C[V.index(a), V.index(b)] = self.G.adj[a][b]['weight']

        print("Matriz de costos:\n", C)

        # Inicialización de S, D y P
        S = set([origen])
        D = {}  # Diccionario de distancias
        P = {}  # Diccionario de predecesores

        # Inicializando distancias
        for i in range(n):
            if V[i] == origen:
                D[V[i]] = 0
            else:
                if (origen, V[i]) in self.G.edges:
                    D[V[i]] = C[V.index(origen), i]
                else:
                    D[V[i]] = np.inf

        # Bucle principal
        Predecesores = {v: {} for v in V}
        for _ in range(n - 1):
            P = {}  # Reiniciando P
            w = min((v for v in V if v not in S), key=lambda v: D[v])
            S.add(w)

            # Actualiza las distancias de los vecinos de w
            for v in V:
                if v not in S and C[V.index(w), V.index(v)] != np.inf:
                    if D[w] + C[V.index(w), V.index(v)] < D[v]:
                        P[v] = w
                        D[v] = D[w] + C[V.index(w), V.index(v)]
                        Predecesores[V[V.index(v)]] = P

        return D, Predecesores

    def floydFunc(self):
        """
        Implementa el algoritmo de Floyd-Warshall para encontrar los caminos más cortos entre todos los pares de nodos.

        :return: Tupla con la matriz de costos y la matriz de predecesores.
        """
        G = self.G
        n = G.number_of_nodes()
        nodos = list(G.nodes)
        P = np.full((n, n), None)
        C = np.full((n, n), np.inf)

        for a, b in G.edges:
            i, j = nodos.index(a), nodos.index(b)
            C[i, j] = G[a][b]['weight']
            P[i, j] = i

        np.fill_diagonal(C, 0)

        # Algoritmo Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if C[i, k] + C[k, j] < C[i, j]:
                        temp = C[i, j]
                        C[i, j] = C[i, k] + C[k, j]
                        P[i, j] = P[k, j]
                        if temp != C[i, j]:
                            print("\nCosto Anterior: ", temp)
                            print(f"{nodos[i]} -> {nodos[j]}: min( {temp}, {nodos[i]}->{nodos[k]}+{nodos[k]}->{nodos[j]} ) ={C[i, j]}")

        return C, P

    def reconstruirCamino(self, C, P, origen, destino):
        """
        Reconstruye el camino más corto entre dos nodos usando la matriz de predecesores.

        :param C: Matriz de costos.
        :param P: Matriz de predecesores.
        :param origen: Nodo de origen.
        :param destino: Nodo de destino.
        :return: Lista de aristas que forman el camino más corto.
        """
        G = self.G
        nodos = list(G.nodes)
        i, j = nodos.index(origen), nodos.index(destino)
        if C[i, j] == np.inf:
            return []

        camino = []
        while j is not None and j != i:
            camino.append((nodos[P[i, j]], nodos[j]))
            j = P[i, j]

        return list(reversed(camino))

    def reconstruirCaminos(self, origen, predecesores: dict):
        """
        Reconstruye todos los caminos más cortos desde un nodo origen usando los predecesores.

        :param origen: Nodo de origen.
        :param predecesores: Diccionario de predecesores.
        :return: Lista de caminos más cortos.
        """
        aristas = []
        for nodo, predecesor in predecesores.items():
            camino = []
            anterior = origen
            destino = None
            for a, b in predecesor.items():
                arista = (anterior, b)
                anterior = b
                destino = a
                camino.append(arista)

            if destino is None:
                if self.G.has_edge(anterior, nodo):
                    camino.append((anterior, nodo))
            else:
                camino.append((anterior, destino))

            aristas.append(camino)

        return aristas

    def dijkstra(self):
        """
        Ejecuta el algoritmo de Dijkstra y muestra los caminos más cortos en la interfaz gráfica.
        """
        origen = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo origen:", parent=self.root)
        self.root.update()
        destino = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo destino, 'todo' para dibujar todos:", parent=self.root)
        if origen in self.G.nodes:
            try:
                if destino != 'todo':
                    self.G.nodes[destino]
                distancias, predecesores = self.dijkstraFunc(origen)
                strDistancia = ""
                for nodo, distancia in distancias.items():
                    strDistancia += (f"{origen} -> {nodo}: {distancia}\n")

                camino = []
                paths = self.reconstruirCaminos(origen, predecesores)
                if destino == 'todo':
                    for path in paths:
                        camino += path
                else:
                    camino = paths[list(self.G.nodes).index(destino)]
                self.camino = camino
                print(self.camino)
                self.dibujar_grafo()
                messagebox.showinfo(message=f"Distancias más cortas de {origen} a todos los nodos:\n{strDistancia}")

            except nx.NetworkXNoPath:
                messagebox.showwarning("Aviso", "No hay camino entre los nodos seleccionados.")
            except KeyError:
                messagebox.showerror("Error", "Asegúrese de que el nodo de destino exista.")
        else:
            messagebox.showerror("Error", "Asegúrese de que el nodo de origen exista.")

    def floyd(self):
        """
        Ejecuta el algoritmo de Floyd-Warshall y muestra los caminos más cortos en la interfaz gráfica.
        """
        strDistancia = ""
        C, P = self.floydFunc()
        nodos = list(self.G.nodes)
        ci, cj = C.shape
        self.caminos = []
        for i in range(ci):
            for j in range(cj):
                if C[i, j] != np.inf and nodos[i] != nodos[j]:
                    strDistancia += (f"{nodos[i]} -> {nodos[j]}: {C[i, j]}\n")
                    camino = self.reconstruirCamino(C, P, nodos[i], nodos[j])
                    self.caminos.append(camino)

        self.dibujar_grafo()
        messagebox.showinfo(message=f"Distancias más cortas de todos los nodos:\n{strDistancia}")

    def siguienteCamino(self):
        """
        Muestra el siguiente camino calculado por Floyd-Warshall en la interfaz gráfica.
        """
        if len(self.caminos) > 0:
            self.camino = self.caminos.pop()
            self.dibujar_grafo()
        else:
            messagebox.showinfo(message="Ya visualizó todos los caminos.")

    def dibujar_grafo(self):
        """
        Dibuja el grafo en la interfaz gráfica, resaltando los caminos más cortos si existen.
        """
        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, node_size=200, node_color='#ff5353')
        nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_family="Montserrat", font_color='white', font_weight='bold')
        edges_diff = set(self.G.edges) - set(self.camino)
        edge_labels_diff = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
        edge_labels = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in self.camino if edge in self.G.edges}
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges_diff, width=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels_diff, font_size=10, font_color='#ff5353', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6})
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.camino, edge_color='#ff5353', width=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_size=10, font_color='#040404', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6})

        self.canvas.draw()

    def on_press(self, event):
        """
        Maneja el evento de presionar el mouse para mover nodos.

        :param event: Evento de presionar el mouse.
        """
        if event.xdata is not None and event.ydata is not None:
            for node, (x, y) in self.pos.items():
                if abs(event.xdata - x) < 0.1 and abs(event.ydata - y) < 0.1:
                    self.dragging = node
                    break

    def on_release(self, event):
        """
        Maneja el evento de soltar el mouse para dejar de mover nodos.

        :param event: Evento de soltar el mouse.
        """
        self.dragging = None

    def on_motion(self, event):
        """
        Maneja el evento de mover el mouse para arrastrar nodos.

        :param event: Evento de mover el mouse.
        """
        if self.dragging and event.xdata is not None and event.ydata is not None:
            self.pos[self.dragging] = (event.xdata, event.ydata)
            self.dibujar_grafo()

# Crear ventana
root = tk.Tk()
app = GrafoInteractivo(root)
root.mainloop()