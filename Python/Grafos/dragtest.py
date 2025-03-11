import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GrafoInteractivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafo Interactivo con Menú")

        # Crear el contenedor para el menú
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Botones del menú
        tk.Button(self.menu_frame, text="Agregar Vértice", command=self.agregar_vertice).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Agregar Arista", command=self.agregar_arista).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Visualizar Caminos", command=self.visualizar_camino).pack(fill=tk.X, pady=5)
        tk.Button(self.menu_frame, text="Salir", command=root.quit).pack(fill=tk.X, pady=20)

        # Crear la figura y el lienzo de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Inicializar el grafo
        self.G = nx.DiGraph()
        self.pos = {}

        # Habilitar movimiento de nodos
        self.dragging = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def agregar_vertice(self):
        nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:")
        if nombre and nombre not in self.G.nodes:
            self.G.add_node(nombre)
            self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
            self.dibujar_grafo()

    def agregar_arista(self):
        origen = simpledialog.askstring("Agregar Arista", "Ingrese el nodo origen:")
        destino = simpledialog.askstring("Agregar Arista", "Ingrese el nodo destino:")
        peso = simpledialog.askfloat("Agregar Arista", "Ingrese el peso de la arista:")
        
        if origen in self.G.nodes and destino in self.G.nodes and peso is not None:
            self.G.add_edge(origen, destino, weight=peso)
            self.dibujar_grafo()
        else:
            messagebox.showerror("Error", "Los nodos deben existir y el peso debe ser válido.")

    def visualizar_camino(self):
        origen = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo origen:")
        destino = simpledialog.askstring("Visualizar Camino", "Ingrese el nodo destino:")
        
        if origen in self.G.nodes and destino in self.G.nodes:
            try:
                path = nx.shortest_path(self.G, source=origen, target=destino, weight="weight")
                edges_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
                self.dibujar_grafo(edges_path)
            except nx.NetworkXNoPath:
                messagebox.showwarning("Aviso", "No hay camino entre los nodos seleccionados.")
        else:
            messagebox.showerror("Error", "Asegúrese de que ambos nodos existen.")

    def dibujar_grafo(self, path_edges=[]):
        self.ax.clear()
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_color="lightblue", edge_color="gray", node_size=700, font_size=10)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=self.ax)
        
        # Resaltar camino más corto
        if path_edges:
            nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges, edge_color="red", width=2, ax=self.ax)
        
        self.canvas.draw()

    def on_press(self, event):
        if event.xdata is not None and event.ydata is not None:
            for node, (x, y) in self.pos.items():
                if abs(event.xdata - x) < 0.1 and abs(event.ydata - y) < 0.1:
                    self.dragging = node
                    break

    def on_release(self, event):
        self.dragging = None

    def on_motion(self, event):
        if self.dragging and event.xdata is not None and event.ydata is not None:
            self.pos[self.dragging] = (event.xdata, event.ydata)
            self.dibujar_grafo()

# Crear ventana
root = tk.Tk()
app = GrafoInteractivo(root)
root.mainloop()
