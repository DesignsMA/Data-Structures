import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GrafoInteractivo:
    """
    Clase para crear y manipular un grafo interactivo con una interfaz gráfica.
    Permite agregar vértices y aristas, ejecutar Dijkstra y Floyd-Warshall,
    y visualizar caminos más cortos.
    """

    def __init__(self, root: tk.Tk):
        """Inicializa la ventana, el grafo y los eventos de la interfaz gráfica."""
        self.root = root
        self.root.title("Grafo Interactivo con Menú")
        self.root.attributes('-topmost', True)
        self.root.focus_force()

        # Menú de opciones
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        opciones = [
            ("Agregar Vértice", self.agregar_vertice),
            ("Agregar Arista", self.agregar_arista),
            ("Dijkstra", self.dijkstra),
            ("Floyd Marshall", self.floyd),
            ("Siguiente camino | Floyd", self.siguienteCamino),
            ("Limpiar resaltado", self.reset),
            ("Salir", root.quit)
        ]
        for texto, comando in opciones:
            tk.Button(self.menu_frame, text=texto, command=comando).pack(fill=tk.X, pady=5)

        # Lienzo de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Inicializar grafo
        self.G = nx.DiGraph()
        self.pos = {}
        self.camino = []
        self.caminos = []
        self.dragging = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def agregar_vertice(self):
        """Solicita al usuario un nombre de vértice y lo añade al grafo."""
        nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:", parent=self.root)
        if nombre and nombre not in self.G.nodes:
            self.G.add_node(nombre)
            self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))
            self.dibujar_grafo()

    def agregar_arista(self):
        """Solicita al usuario dos nodos y un peso para agregar una arista."""
        origen = simpledialog.askstring("Agregar Arista", "Ingrese el nodo origen:", parent=self.root)
        destino = simpledialog.askstring("Agregar Arista", "Ingrese el nodo destino:", parent=self.root)
        peso = simpledialog.askfloat("Agregar Arista", "Ingrese el peso de la arista:", parent=self.root)
        
        if origen in self.G.nodes and destino in self.G.nodes and peso is not None:
            if peso >= 0:
                self.G.add_edge(origen, destino, weight=peso)
                self.dibujar_grafo()
            else:
                messagebox.showerror("Error", "El peso debe ser válido (0-Inf).")
        else:
            messagebox.showerror("Error", "Los nodos deben existir y el peso debe ser válido (0-Inf).")

    def reset(self):
        """Limpia el resaltado del camino en el grafo."""
        self.ax.clear()
        self.camino = []
        self.dibujar_grafo()

    def dijkstra(self):
        """Ejecuta el algoritmo de Dijkstra y visualiza los caminos más cortos."""
        origen = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo origen:", parent=self.root)
        destino = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo destino, 'todo' para dibujar todos:", parent=self.root)
        if origen in self.G.nodes:
            try:
                if destino != 'todo':
                    self.G.nodes[destino]
                distancias, predecesores = self.dijkstraFunc(origen)
                strDistancia = "\n".join(f"{origen} -> {nodo}: {distancia}" for nodo, distancia in distancias.items())
                
                camino = []
                paths = self.reconstruirCaminos(origen, predecesores)
                if destino == 'todo':
                    for path in paths:
                        camino += path
                else:
                    camino = paths[list(self.G.nodes).index(destino)]
                
                self.camino = camino
                self.dibujar_grafo()
                messagebox.showinfo(message=f"Distancias más cortas:\n{strDistancia}")
            except nx.NetworkXNoPath:
                messagebox.showwarning("Aviso", "No hay camino entre los nodos seleccionados.")
            except KeyError:
                messagebox.showerror("Error", "Asegúrese de que el nodo de destino exista.")
        else:
            messagebox.showerror("Error", "Asegúrese de que el nodo de origen exista.")
    
    def dibujar_grafo(self):
        """Dibuja el grafo y resalta los caminos más cortos si existen."""
        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, node_size=200, node_color='#ff5353')
        nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_color='white')
        edges_diff = set(self.G.edges) - set(self.camino)
        edge_labels_diff = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
        edge_labels = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in self.camino if edge in self.G.edges}
        
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges_diff, width=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels_diff, font_size=10)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.camino, edge_color='#ff5353', width=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_size=10, font_color='#040404')
        self.canvas.draw()
    
    def on_press(self, event):
        """Detecta si se ha presionado sobre un nodo para arrastrarlo."""
        if event.xdata and event.ydata:
            for node, (x, y) in self.pos.items():
                if abs(event.xdata - x) < 0.1 and abs(event.ydata - y) < 0.1:
                    self.dragging = node
                    break

    def on_release(self, event):
        """Libera el nodo arrastrado."""
        self.dragging = None

    def on_motion(self, event):
        """Mueve un nodo al arrastrarlo."""
        if self.dragging and event.xdata and event.ydata:
            self.pos[self.dragging] = (event.xdata, event.ydata)
            self.dibujar_grafo()

# Ejecutar aplicación
root = tk.Tk()
app = GrafoInteractivo(root)
root.mainloop()
