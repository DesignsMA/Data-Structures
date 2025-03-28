import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Ruta base (ej: "C:/grafo/")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class GrafoInteractivo:


    def __init__(self, root: ttk.Window):
        """
        Inicializa la interfaz gráfica y configura el grafo interactivo.

        :param root: Ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("ALGORITMOS | MST")
        self.root.attributes('-topmost', True)  # Mantener en primer plano
        self.root.focus_force()  # Forzar el foco en la ventana

        # Crear el contenedor para el menú
        self.menu_frame = ttk.Frame(self.root)
        self.menu_frame.pack(side=ttk.LEFT, fill=ttk.Y, padx=10, pady=10)

        # Botones del menú
        ttk.Button(self.menu_frame, text="Cargar archivo de zonas", bootstyle=DANGER, command=self.cargarGrafo).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Agregar Zona de bosques", bootstyle=DANGER, command=self.agregar_vertice).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Agregar/Actualizar ruta a una zona", bootstyle=DANGER, command=self.agregar_arista).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Reiniciar vista", bootstyle=SUCCESS, command=self.reset).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Salir", bootstyle=INFO, command=root.quit).pack(fill=ttk.X, pady=20)
        # Crear la figura y el lienzo de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Elimina los márgenes

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=ttk.RIGHT, fill=ttk.BOTH, expand=True)

        # Inicializar el grafo
        self.G = nx.Graph()
        self.pos = {}  # Posiciones de los nodos
        self.resaltado = []
        self.isModifiable = True
        self.temp = []

        # Habilitar movimiento de nodos
        self.dragging = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def cargarGrafo(self):
        ruta = simpledialog.askstring(
        "Cargar zonas", 
        "Ingrese la ruta relativa (ej: Zonas/Zonas.txt):", 
        parent=self.root
    )
        if ruta:
            try:
                # Combinar la ruta base con la ruta relativa
                ruta_absoluta = os.path.join(BASE_DIR, ruta)
                with open(ruta_absoluta, "r", encoding="UTF-8") as file:
                    # Leer tipo de grafo
                    primera_linea = file.readline().strip()
                    if primera_linea not in ['True', 'False']:
                        raise ValueError("La primera línea debe ser 'True' o 'False' para indicar si es dirigido")
                    isDiGraph = primera_linea == 'True'

                    # Leer nodos
                    segunda_linea = file.readline().strip()
                    if not segunda_linea:
                        raise ValueError("Falta la línea de nombres de nodos")
                    nodos = segunda_linea.split(',')

                    # Leer matriz de adyacencia
                    matriz = []
                    for i, linea in enumerate(file):
                        valores = linea.strip().split(',')
                        if len(valores) != len(nodos):
                            raise ValueError(f"La fila {i+3} no tiene el número correcto de columnas")
                        try:
                            fila = [float(val) if val else 0.0 for val in valores]
                        except ValueError:
                            raise ValueError(f"Valor no numérico en la fila {i+3}")
                        matriz.append(fila)

                    # Verificar matriz cuadrada
                    if len(matriz) != len(nodos):
                        raise ValueError("La matriz de adyacencia no es cuadrada")

                    # Crear grafo
                    G = nx.DiGraph() if isDiGraph else nx.Graph()
                    G.add_nodes_from(nodos)

                    # Añadir aristas con pesos
                    for i in range(len(nodos)):
                        for j in range(len(nodos)):
                            peso = matriz[i][j]
                            if peso != 0:
                                if isDiGraph or (not isDiGraph and i <= j):
                                    if nodos[i] == nodos[j]:
                                        raise ValueError(f"Columna {i} | Fila {j}\nNo puede haber una ruta a si mismo.")
                                    G.add_edge(nodos[i], nodos[j], weight=peso)

                    self.G = G # cargar grafo
                    self.pos = nx.bfs_layers(self.G,sources=list(self.G.nodes)[0])
                    self.dibujar_grafo()

            except FileNotFoundError:
                messagebox.showerror(message=f"Error: No se encontró el archivo en la ruta {ruta}")
            except ValueError as ve:
                messagebox.showerror(message=f"Error en el formato del archivo: {ve}")
            except Exception as e:
                messagebox.showerror(message=f"Error inesperado: {e}")
            return None

    def agregar_vertice(self):
        """
        Agrega un vértice al grafo. Solicita al usuario el nombre del vértice.
        """
        if self.isModifiable:
            nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:", parent=self.root)
            if nombre and nombre not in self.G.nodes:
                self.G.add_node(nombre)
                self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
                self.dibujar_grafo()
        else:
            messagebox.showerror(message="Actualmente solo esta visualizando el árbol generado.")

    def agregar_arista(self):
        """
        Agrega una arista al grafo. Solicita al usuario el nodo origen, nodo destino y peso de la arista.
        """
        if self.isModifiable:
            origen = simpledialog.askstring("Agregar Arista", "Ingrese el nodo origen:", parent=self.root)
            self.root.update()  # Actualizar la ventana
            destino = simpledialog.askstring("Agregar Arista", "Ingrese el nodo destino:", parent=self.root)
            self.root.update()  # Actualizar la ventana
            peso = simpledialog.askfloat("Agregar Arista", "Ingrese el peso de la arista:", parent=self.root)

            if origen in self.G.nodes and destino in self.G.nodes and peso:
                if origen == destino:
                    messagebox.showerror("Error", "No puede haber una ruta a si mismo.")
                    return
                if peso >= 0:
                    self.G.add_edge(origen, destino, weight=peso)
                    self.dibujar_grafo()
                else:
                    messagebox.showerror("Error", "El peso debe ser válido (0-Inf).")
            else:
                messagebox.showerror("Error", "Los nodos deben existir y el peso debe ser válido (0-Inf).")
        else:
            messagebox.showerror(message="Actualmente solo esta visualizando el árbol generado.")
    
    def generar_posiciones_arbol(self,G: nx.Graph, root):
        niveles = {}  # Diccionario para almacenar niveles de cada nodo
        posiciones = {}  # Diccionario de posiciones finales
        visitados = set()  # Para evitar ciclos

        # Obtener estructura de árbol (suponiendo que G es un árbol o un MST)
        arbol = nx.bfs_tree(G, root)  # Usa búsqueda en anchura (BFS) para formar un árbol desde root

        def dfs(nodo, nivel=0, x=0, ancho=1):
            if nodo in visitados:
                return
            visitados.add(nodo)
            niveles[nodo] = nivel
            posiciones[nodo] = (x, -nivel)  # -nivel para que crezca hacia abajo

            hijos = list(arbol[nodo])  # Solo tomamos los hijos en el árbol BFS
            num_hijos = len(hijos)

            for i, hijo in enumerate(hijos):
                dfs(hijo, nivel + 1, x + (i - (num_hijos - 1) / 2) * ancho / 2, ancho / 2)

        dfs(root)
        return posiciones            
    
    def reset(self):
        """
        Reiniciar la vista.
        """
        if len(self.temp) > 0:
            self.G, self.pos = self.temp
            self.resaltado = []
            self.isModifiable = True
            self.temp = []
        self.dibujar_grafo()

    def dibujar_grafo(self, optColor:str="#ffc600"):
        """
        Dibuja el grafo en la interfaz gráfica, resaltando aristas si se proveen.
        """
        self.ax.clear()
        nx.draw_networkx_nodes(self.G, self.pos, node_size=200, node_color='#ff5353')
        nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_family="Montserrat", font_color='white', font_weight='bold')
        edges_diff = set(self.G.edges) - set(self.resaltado)
        edge_labels_diff = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
        edge_labels = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in self.resaltado if edge in self.G.edges}
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges_diff, width=2)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels_diff, font_size=10, font_color='#ff5353', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6})
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.resaltado, edge_color=optColor, width=3)
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
            
root = ttk.Window(themename="darkly") 

app = GrafoInteractivo(root)
root.mainloop()