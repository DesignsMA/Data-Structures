import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time as time

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
        ttk.Button(self.menu_frame, text="Cargar grafo por defecto", bootstyle=DANGER, command=self.default).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Agregar Vértice", bootstyle=DANGER, command=self.agregar_vertice).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Agregar/Actualizar Arista", bootstyle=DANGER, command=self.agregar_arista).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Generar árbol de expansión mínima | Kruskal", bootstyle=INFO, command=self.kruskal).pack(fill=ttk.X, pady=5)
        ttk.Button(self.menu_frame, text="Generar árbol de expansión mínima | Prim", bootstyle=INFO, command=self.prim_mst).pack(fill=ttk.X, pady=5)
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

    def default(self):
        if self.isModifiable:
            self.G = nx.Graph()
            self.G.add_edges_from([
            ('A', 'B', {'weight': 1.0}),
            ('B', 'C', {'weight': 2.0}),
            ('C', 'D', {'weight': 3.0}),
            ('D', 'A', {'weight': 4.0}),
            ('A', 'C', {'weight': 5.0}),
            ('A', 'E', {'weight': 15.0}),
            ('B', 'D', {'weight': 6.0}),
            ('C', 'E', {'weight': 7.0})
        ])
            self.pos = nx.spring_layout(self.G, k=0.5, iterations=100)
            self.dibujar_grafo()
        else:
            messagebox.showerror(message="Actualmente solo esta visualizando el árbol generado.")

        
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

    def kruskal(self):
        if self.isModifiable:
            G = self.G
            if not G.is_directed() and nx.is_connected(G):  # Si el grafo es conexo y no dirigido
                V = set(G.nodes)  # Conjunto de vértices
                # Estructura para manejar las componentes conexas (Union-Find)
                C = {}  # Diccionario para almacenar el padre de cada vértice

                def INICIAL(v):
                    """Inicializa una componente conexa para el vértice v."""
                    C[v] = v  # Cada vértice es su propio padre inicialmente

                def ENCUENTRA(v):
                    """Encuentra la componente conexa a la que pertenece el vértice v."""
                    if C[v] != v:
                        C[v] = ENCUENTRA(C[v])  # Compresión de camino
                    return C[v]

                def COMBINA(u, v):
                    """Combina las componentes conexas de u y v."""
                    root_u = ENCUENTRA(u)
                    root_v = ENCUENTRA(v)
                    if root_u != root_v:
                        C[root_v] = root_u  # Une las componentes

                # Inicializar componentes para cada vértice
                for v in V:
                    INICIAL(v)

                # Lista ordenada de las aristas por peso
                A = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
                MST = nx.Graph()  # Grafo resultante para el árbol
                start = list(self.G.nodes)[0]
                self.temp = [self.G, self.pos]
                self.G = MST
                self.isModifiable = False
                messagebox.showinfo("Proceso comenzado", "En dorado vera la arista actual, en rojo aquellas que son descartadas.")
                def agregar_arista_a_MST():
                    if len(A) > 0:
                        u, v, weight = A.pop(0)  # Obtener la arista con el menor peso
                        print(f"({u},{v},{weight})")
                        self.resaltado = [(u,v)]  # Resaltar las aristas del MST
                        if ENCUENTRA(u) != ENCUENTRA(v):  # Si no forman un ciclo
                            MST.add_edge(u, v, **weight)  # Añadir la arista al MST
                            COMBINA(u, v)  # Combinar las componentes

                            # Actualizar visualización
                            self.pos = self.generar_posiciones_arbol(self.G, start)
                            self.dibujar_grafo()  # Dibujar el grafo actualizado
                            self.root.after(2000, agregar_arista_a_MST)
                        else:
                            self.dibujar_grafo('red')  # Dibujar el grafo actualizado
                                # Llamar a la función de nuevo después de 1 segundo
                            self.root.after(2000, agregar_arista_a_MST)
                    else:
                        # Cuando todas las aristas han sido procesadas
                        messagebox.showinfo("Proceso completado", "El árbol de expansión mínima ha sido encontrado.")
                        self.resaltado = list(self.G.edges)
                        self.dibujar_grafo()

                # Iniciar el proceso de construcción del MST
                if len(A) > 0 :
                    agregar_arista_a_MST()

            else:
                messagebox.showerror(message="El grafo debe ser no dirigido y conexo.")
        else:
            messagebox.showerror(message="Actualmente solo esta visualizando el árbol generado.")


    def prim_mst(self):
        if self.isModifiable:
            start = simpledialog.askstring("Introduzca lo pedido", "Ingrese el nodo de inicio:", parent=self.root)
            self.root.update()  # Actualizar la ventana
    
            G = self.G
            if start not in G.nodes:
                messagebox.showerror(message="El nodo de inicio no existe en el grafo.")
                return
    
            U = {start}  # Conjunto de nodos en el MST
            Tree = nx.Graph()  # Grafo resultante para el árbol de expansión mínima
            aristas_candidatas = []
            self.temp = [self.G, self.pos]
            self.G = Tree
            self.isModifiable = False
            def actualizar_arista():
                if len(U) < len(G.nodes):
                    # Limpiar las aristas candidatas de la iteración anterior
                    aristas_candidatas.clear()
    
                    # Recopilar todas las aristas candidatas de los nodos en U
                    for nodo in U:
                        for vecino, atributos in G[nodo].items():
                            if vecino not in U:
                                if "weight" not in atributos:
                                    raise ValueError(f"La arista {nodo}-{vecino} no tiene peso.")
                                aristas_candidatas.append((nodo, vecino, atributos["weight"]))
    
                    if not aristas_candidatas:
                        messagebox.showerror(message="El grafo no es conexo, no se puede formar un árbol de expansión mínima.")
                        return
    
                    # Seleccionar la arista de menor peso
                    nodo1, nodo2, peso = min(aristas_candidatas, key=lambda x: x[2])
    
                    # Agregar la arista al árbol de expansión mínima
                    Tree.add_edge(nodo1, nodo2, weight=peso)
                    self.pos = self.generar_posiciones_arbol(self.G, start)
                    self.resaltado = [(nodo1, nodo2)]  # Para resaltar la arista en la interfaz
                    self.dibujar_grafo()  # Actualizar el dibujo del grafo
    
                    U.add(nodo2)  # Agregar el nodo al conjunto U
    
                    # Llamar de nuevo después de 1 segundo para la siguiente iteración
                    self.root.after(2000, actualizar_arista)
                else:
                    messagebox.showinfo("Proceso completado", "El árbol de expansión mínima ha sido encontrado.")
                    self.resaltado = list(Tree.edges)
                    self.dibujar_grafo()
    
            # Iniciar el proceso de encontrar el MST
            actualizar_arista()
            
        else:
            messagebox.showerror(message="Actualmente solo esta visualizando el árbol generado.")
            
    
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
            

# Crear ventana con ttkbootstrap (nuevo enfoque)
root = ttk.Window(themename="darkly")  # Cambia "darkly" por el tema que prefieras

app = GrafoInteractivo(root)
root.mainloop()