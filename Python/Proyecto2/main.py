import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from math import sqrt
import random
from Resources import dstheme
dstheme.__main__()
# Ruta base (ej: "C:/grafo/")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class GuardianesBosque:

    def __init__(self, root: ttk.Window):
        """
        Inicializa la interfaz gráfica.
        
        :param root: Ventana principal de la aplicación.
        """
        self.root = root
        self._configurar_fuentes()
        self._configurar_ventana()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True) # crando frame inicial
        self._crear_ventana_bienvenida()
        self._crear_menu_frame()  # Separamos la creación del menú
        self._crear_area_grafico() # Se añade el gráfico al menu frame
        self._inicializar_grafo()
        self.menu_frame.grid_remove()
        
    def _configurar_fuentes(self):
        """Configura las fuentes globales"""
        font = "Montserrat Bold"
        self.root.style.configure('.', font=(font, 10))
        self.root.option_add('*TCombobox*Listbox.font', (font, 10))
        self.root.option_add('*TCombobox.font', (font, 10))
        self.root.option_add('*TEntry.font', (font, 10))
        self.root.option_add('*TSpinbox.font', (font, 10))
    
    def _configurar_ventana(self):
        """Configura propiedades de la ventana"""
        self.root.attributes('-topmost', True)
        self.root.focus_force()
    
    def _crear_ventana_bienvenida(self):
        self.bienvenida_frame = ttk.Frame(self.main_frame, width=1200)
        self.bienvenida_frame.grid(row=0,column=0)
        label1 = ttk.Label(self.bienvenida_frame, text="BIENVENIDO A GUARDIANES DEL BOSQUE", font=("Montserrat Bold",35),foreground="#0fff6f", justify="center").grid(row=0,column=0, pady=30)
        intro_text = """🌿 Descubre como proteger nuestros ecosistemas con algoritmos 🌿 

En esta capacitación, aprenderás a:
• Explorar zonas contaminadas
• Optimizar rutas de recolección de residuos
• Diseñar redes de reciclaje

Al completar las actividades, recibirás un
Certificado Digital como 'Guardián del Bosque'"""

        intro_label = ttk.Label(
            master=self.bienvenida_frame,
            text=intro_text,
            font=("Montserrat Light", 18),
            justify="center",
        ).grid(row=1,column=0)

        btn = ttk.Button(self.bienvenida_frame, text="Estoy Listo!", style=DANGER, command=self.continuar, width=40).grid(row=2,column=0, pady=30)

    def continuar(self):
        self.toggle_mostrar_ocultar(self.bienvenida_frame)
        self.toggle_mostrar_ocultar(self.menu_frame)
        
    def _crear_menu_frame(self):
        """Crea y organiza el frame del menú usando grid"""
        self.menu_frame = ttk.Frame(self.main_frame, width=200)
        # Frame de botones
        self.button_frame = ttk.Frame(self.menu_frame)
        self.menu_frame.grid(row=1, column=0, sticky='nswe')
        
        self.button_frame.grid(row=0, column=0, sticky='ew') # colocar botones en fila 0
        # Botones del menú (organizados en grid)
        
        botones = [
            ("Cargar archivo de zonas", PRIMARY, self.cargarGrafo),
            ("Agregar Zona de bosques", PRIMARY, self.agregar_vertice),
            ("Agregar/Actualizar ruta a una zona", PRIMARY, self.agregar_arista),
            ("Salir", SECONDARY, self.root.quit)
        ]
        
        for i, (texto, estilo, comando) in enumerate(botones):
            ttk.Button(
                self.button_frame,
                text=texto,
                bootstyle=estilo,
                command=comando
            ).grid(row=i, column=0, sticky='ew', pady=5)

    
    def _crear_area_grafico(self):
        """Crea el área del gráfico a la derecha en menu_frame"""
        # Frame para el gráfico (derecha)
        self.graph_frame = ttk.Frame(self.menu_frame) 
        self.graph_frame.grid(row=0, column=1, sticky='nswe', padx=10) # colocar grafo en columna 1
        
        # Crear figura de Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Canvas para el gráfico
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Eventos del mouse
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
    
    def toggle_mostrar_ocultar(self, target: ttk.Frame):
        """
        Muestra u oculta un ttk.Frame (target) con una disposición de grid pero sin olvidar las posiciones.
        """
        print(target)
        if target.winfo_viewable():
            target.grid_remove()
        else:
            target.grid()
    
    def _inicializar_grafo(self):
        """Inicializa el grafo y variables de estado"""
        self.G = nx.Graph()
        self.pos = {}
        self.resaltado = []
        self.contaminadas = []
        self.isModifiable = True
        self.dragging = None

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
                    self.pos = nx.spring_layout(self.G, scale=1.6, k=3/sqrt(G.number_of_nodes()))
                    self.dibujar_grafo()

            except FileNotFoundError:
                messagebox.showerror(message=f"Error: No se encontró el archivo en la ruta {ruta}")
            except ValueError as ve:
                messagebox.showerror(message=f"Error en el formato del archivo: {ve}")
            except Exception as e:
                messagebox.showerror(message=f"Error inesperado: {e}")
            return None
    
    def asignar_zonas_contaminadas(self):
        if self.isModifiable and self.G.number_of_nodes() > 2:
            grafo = self.G
            vertices = list(grafo.nodes)

            num_zonas_contaminadas = random.randint(1, len(vertices)-1)

            zonas_contaminadas = set()

            while len(zonas_contaminadas) < num_zonas_contaminadas:
                zona = random.choice(vertices)
                if zona not in zonas_contaminadas:
                    zonas_contaminadas.add(zona)
            self.contaminadas = zonas_contaminadas

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
            elif nombre in self.G.nodes:
                messagebox.showerror(message="Ya existe esa zona.")
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
        nx.draw_networkx_nodes(self.G, self.pos, node_size=400, node_color='#00ff99')
        nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_family="Montserrat", font_color='#164435', font_weight='bold')
        edges_diff = set(self.G.edges) - set(self.resaltado)
        edge_labels_diff = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
        edge_labels = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in self.resaltado if edge in self.G.edges}
        print(edge_labels_diff)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=edges_diff, width=3)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels_diff, font_size=10, font_color='#040404', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6})
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.resaltado, edge_color=optColor, width=3)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_size=10, font_color=optColor, font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.8})

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
            
root = ttk.Window(themename="dstheme") 

app = GuardianesBosque(root)
root.title("Guardianes del Bosque")

root.mainloop()