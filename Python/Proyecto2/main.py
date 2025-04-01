import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from math import sqrt
from PIL import Image, ImageTk
import random
from Resources import dstheme
from Scripts import *
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
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True) # crando frame inicial
        self._configurar_ventana()
        self._crear_ventana_bienvenida()
        self._crear_menu_frame()  # Separamos la creación del menú
        self._crear_area_grafico() # Se añade el gráfico al menu frame
        self._inicializar_grafo()
        self._definirActividades()
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
        self.root.state('zoomed')  # Para Windows
        # Configuración de expansión de la ventana principal
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def _inicializar_grafo(self):
        """Inicializa el grafo y variables de estado"""
        self.G = nx.Graph()
        self.H = nx.Graph()
        self.pos = {}
        self.secondary_pos = {}
        self.resaltado = []
        self.contaminadas = set()
        self.roadmap = set()
        self.isModifiable = True
        self.dragging = None
        self.secondary_dragging = None
        
    def load_image(self):
        try:
            # Cambia esta ruta por tu imagen
            image_path = os.path.join(BASE_DIR, "Resources/shield.png")  
            self.img = Image.open(image_path)
            self.img = self.img.resize((int(self.img.width*0.5), int(self.img.height*0.5)), Image.LANCZOS)  # Ajusta tamaño
            self.tk_img = ImageTk.PhotoImage(self.img)
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            self.tk_img = None
    
    def _crear_ventana_bienvenida(self):
        self.load_image()

        # Frame principal que ocupará toda la ventana
        self.bienvenida_frame = ttk.Frame(self.main_frame)
        self.bienvenida_frame.grid(row=0, column=0, sticky="nsew")

        # Configuración para centrado perfecto
        self.bienvenida_frame.grid_rowconfigure(0, weight=1)  # Espacio superior
        self.bienvenida_frame.grid_rowconfigure(1, weight=0)  # Contenido
        self.bienvenida_frame.grid_rowconfigure(2, weight=1)  # Espacio inferior
        self.bienvenida_frame.grid_columnconfigure(0, weight=1)  # Centrado horizontal


        # Frame interno para el contenido (centrado)
        contenido_frame = ttk.Frame(self.bienvenida_frame)
        contenido_frame.grid(row=0, column=0, sticky="")

        # Título principal
        label1 = ttk.Label(
            contenido_frame, 
            text="BIENVENIDO A GUARDIANES DEL BOSQUE", 
            font=("Montserrat Bold", 35),
            foreground="#0fff6f", 
            justify="center"
        )
        label1.grid(row=0, column=0, pady=(0, 20))

        # Texto de introducción
        intro_text = """🌿 Descubre como proteger nuestros ecosistemas con algoritmos 🌿 

En esta capacitación, aprenderás a:
• Explorar zonas contaminadas
• Optimizar rutas de recolección de residuos
• Diseñar redes de reciclaje

Al completar las actividades, recibirás un
Certificado Digital como 'Guardián del Bosque'

Para completar una actividad deberás:
• Acceder a todas las actividades
• Usar cada función exitosamente

Cuando todas las actividades se completen
aparecerá un botón al final para generar
tu certificado.
"""
        intro_label = ttk.Label(
            master=contenido_frame,
            text=intro_text,
            font=("Montserrat Light", 14),
            justify="center",
            image=self.tk_img,
            compound="center"
        )
        intro_label.grid(row=1, column=0, pady=20)

        # Botón de acción
        btn = ttk.Button(
            contenido_frame, 
            text="Estoy Listo!", 
            style=DANGER, 
            command=self.continuar, 
            width=40
        )
        btn.grid(row=2, column=0, pady=(20, 0))

    def continuar(self):
        self.toggle_mostrar_ocultar(self.bienvenida_frame)
        self.toggle_mostrar_ocultar(self.menu_frame)
        
    def _crear_menu_frame(self):
        """Crea y organiza el frame del menú usando grid"""
        self.menu_frame = ttk.Frame(self.main_frame, padding=30)
        # Frame de botones
        self.button_frame = ttk.Frame(self.menu_frame)
        self.menu_frame.grid(row=1, column=0, sticky='nswe')
        
        self.button_frame.grid(row=0, column=0, sticky='ew') # colocar botones en fila 0
        # Botones del menú (organizados en grid)
        
        botones = [
            ("Cargar archivo de zonas", PRIMARY, self.cargarGrafo),
            ("Agregar Zona de bosques", PRIMARY, self.agregar_vertice),
            ("Agregar/Actualizar ruta a una zona", PRIMARY, self.agregar_arista),
            ("Generar nuevas zonas contaminadas", PRIMARY, self.asignar_zonas_contaminadas),
            ("Exploración de zonas", DANGER, lambda: self.mostrarActividad(0)),
            ("Optimización de rutas de recolección", DANGER, lambda: self.mostrarActividad(1)),
            ("Diseño de redes ecológicas", DANGER, lambda: self.mostrarActividad(2)),
            ("Salir", SECONDARY, self.root.quit)
        ]
        self.funcionesBtn = []  # Referencia a botones

        for i, (texto, estilo, comando) in enumerate(botones):
            btn = ttk.Button(
                self.button_frame,
                text=texto,
                bootstyle=estilo,
                command=comando,
            )
            btn.grid(row=i, column=0, sticky='ew', pady=10)
            self.funcionesBtn.append(btn)  # Guardamos la referencia al botón
            
    def _crear_area_grafico(self):
        """Crea el área del gráfico con dos figuras (una visible, otra oculta)"""
        # Frame contenedor principal
        self.graph_frame = ttk.Frame(self.menu_frame)
        self.graph_frame.grid(row=0, column=1, sticky='nsew', padx=3)

        # Frame para figura principal (visible)
        self.main_graph = ttk.Frame(self.graph_frame)
        self.main_graph.grid(row=0, column=0, sticky='nsew')

        # Frame para figura secundaria (oculta inicialmente)
        self.secondary_graph = ttk.Frame(self.graph_frame)
        self.secondary_graph.grid(row=0, column=1, sticky='nsew')
        self.secondary_graph.grid_remove()

        # Crear figura principal
        self._configurar_figura(principal=True)

        # Crear figura secundaria (oculta)
        self._configurar_figura(principal=False)

    def _configurar_figura(self, principal=True):
        """Configura una figura matplotlib con parámetros comunes"""
        frame = self.main_graph if principal else self.secondary_graph
        fig, ax = plt.subplots(facecolor='none')
        ax.set_facecolor('none')
        ax.axis('off')
        fig.tight_layout() # automaticamente ajustar figura
        fig.set_size_inches(10 if principal else 4, 7) 

        # Configuración del canvas
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Eventos del mouse solo para figura principal
        if principal:
                # Conectar eventos a figura principal
                canvas.mpl_connect("button_press_event", 
                                  lambda e: self.on_press(e, self.pos, 'dragging'))
                canvas.mpl_connect("button_release_event", 
                                  lambda e: self.on_release(e, 'dragging'))
                canvas.mpl_connect("motion_notify_event", 
                                  lambda e: self.on_motion(e, self.pos, 'dragging',
                                                        self.G, ax, canvas,
                                                        self.resaltado, self.contaminadas))
                self.fig, self.ax, self.canvas = fig, ax, canvas
                self.dragging = None  # Estado de arrastre para figura principal
        else:
                # Conectar eventos a figura secundaria
                canvas.mpl_connect("button_press_event", 
                                  lambda e: self.on_press(e, self.secondary_pos, 'secondary_dragging'))
                canvas.mpl_connect("button_release_event", 
                                  lambda e: self.on_release(e, 'secondary_dragging'))
                canvas.mpl_connect("motion_notify_event", 
                                  lambda e: self.on_motion(e, self.secondary_pos, 'secondary_dragging',
                                                        self.H, ax, canvas,
                                                        self.resaltado, self.contaminadas))
                self.secondary_fig, self.secondary_ax, self.secondary_canvas = fig, ax, canvas
                self.secondary_dragging = None  # Estado de arrastre para figura secundaria            
    def _definirActividades(self):
                # Definición de actividades
        self.actividades = []

        # Actividad 1
        actividad1 = {
            "titulo":"""🔍 Actividad 1: Exploración de Ecosistemas""",

            "texto": """Objetivo: Identificar y recorrer eficientemente alguna zona contaminada para planificar la recolección de residuos.

Metodos:

BFS (Recorrido en Anchura):
Encontrarás la zona contaminada más cercana a tu ubicación inicial.
Ideal para actuar rapidamente

DFS (Recorrido en Profundidad):
Explorarás rutas complejas para detectar contaminación oculta o extendida.
Ideal para evaluar impactos ambientales a largo plazo.""",
            "botones": [
                ("BFS | Recorrido a lo ancho", PRIMARY, self.bfs),
                ("DFS | Recorrido a lo profundo", PRIMARY, None),
                ("Volver", DANGER, lambda: self.volver(0))
            ]
        }
        
        actividad2 = {
            "titulo":"""🔍 Actividad 2: Optimización de rutas de recolección""",
            "texto": """Objetivo:
Determinar la mejor ruta para transportar residuos a los centros de reciclaje con el menor costo posible.
Los camiones o recolectores siguen estas rutas optimizadas para minimizar costos de transporte.

Métodos:

Dijkstra: Encuentra la ruta más corta desde un punto específico. Encuentra la zona contaminada más
cercana desde un punto inicial, útil si la contaminación es dispersa.

Floyd-Warshall: Encuentra las rutas más cortas entre todas las estaciones de recolección. útil si hay varias
zonas contaminadas conectadas entre sí.""",
            "botones": [
                ("Dijkstra", PRIMARY, None),
                ("Floyd-Warshall", PRIMARY, None),
                ("Volver", DANGER, lambda: self.mostrarActividad(1))
            ]
        }
        
        actividad3 = {
            "titulo":"""🔍 Actividad 3: Diseño de redes ecológicas""",
            "texto": """Objetivo:
Construir un sistema eficiente de estaciones de reciclaje con la menor cantidad de recursos. Las estaciones
de reciclaje serán ubicadas dentro de las zonas identificadas.

Métodos:

Prim: Es útil si las conexiones entre zonas son numerosas, es decir se tiene un bosque denso. Si el número
de zonas E es cercano al número máximo posible de caminos (V(V−1)) /2, el bosque es denso.

Kruskal: Se usa si las zonas están muy dispersas y hay pocos caminos. Si el número de caminos E es
cercano a la cantidad mínima () necesaria para conectar todas las zonas (V−1), el bosque es disperso.""",

            "botones": [
                ("Prim", PRIMARY, self.prim),
                ("Kruskal", PRIMARY, None),
                ("Densidad del bosque", PRIMARY, None),
                ("Volver", DANGER, lambda: self.mostrarActividad(2))
            ]
        }

        # Función para crear actividades
        def crear_actividad(actividad, row_start=0):
            widgets = []

            # Crear label
            ttl = ttk.Label(
                master=self.button_frame,
                text=actividad["titulo"],
                font=("Montserrat Bold", 13),
                justify="center",
                wraplength=400,
                padding=2
            )
            ttl.grid(row=row_start, pady=10)
            widgets.append(ttl)
            lbl = ttk.Label(
                master=self.button_frame,
                text=actividad["texto"],
                font=("Montserrat Light", 11),
                justify="left",
                wraplength=400,
            )
            lbl.grid(row=row_start+1, pady=30)
            widgets.append(lbl)

            # Crear botones
            for i, (texto, estilo, comando) in enumerate(actividad["botones"], start=2):
                btn = ttk.Button(
                    self.button_frame,
                    text=texto,
                    style=estilo,
                    width=30,
                    command= comando
                )
                btn.grid(row=row_start+i, pady=5)
                widgets.append(btn)

            return widgets

        # Crear todas las actividades
        self.actividades.append(crear_actividad(actividad1))
        self.actividades.append(crear_actividad(actividad2))
        self.actividades.append(crear_actividad(actividad3))

        # Ocultar todas las actividades inicialmente
        for actividad in self.actividades:
            for widget in actividad:
                widget.grid_remove()

    def mostrarActividad(self, id):
        for btn in self.funcionesBtn:
            self.toggle_mostrar_ocultar(btn) # ocultar o mostrar botones
        
        for widget in self.actividades[id]:
            self.toggle_mostrar_ocultar(widget)
    
    def prim(self):
        # 1. Cambiar el tamaño de la figura
        self.fig.set_size_inches(5, 7)  # Nuevo tamaño en pulgadas (ancho, alto)

        # 3. Actualizar el canvas
        self.canvas.draw()  # Esto fuerza el redibujado

        # 4. Reconfigurar el widget en Tkinter 
        self.canvas.get_tk_widget().config(width=int(5*self.fig.dpi), height=int(7*self.fig.dpi))
        self.toggle_mostrar_ocultar(self.secondary_graph)
        self.H = self.G
        self.secondary_pos = self.generar_posiciones_arbol(self.H,'A')
        self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas)
            
    def toggle_mostrar_ocultar(self, target: ttk.Frame):
        """
        Muestra u oculta un widget (target) con una disposición de grid pero sin olvidar las posiciones.
        """
        if target.winfo_viewable():
            target.grid_remove()
        else:
            target.grid()
            
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
                    self.asignar_zonas_contaminadas()
                    
            except FileNotFoundError:
                messagebox.showerror(message=f"Error: No se encontró el archivo en la ruta {ruta}")
            except ValueError as ve:
                messagebox.showerror(message=f"Error en el formato del archivo: {ve}")
            #except Exception as e:
            #    messagebox.showerror(message=f"Error inesperado: {e}")
            return None
    
    def asignar_zonas_contaminadas(self):
        if self.isModifiable and self.G.number_of_nodes() > 2:
            grafo = self.G
            vertices = list(grafo.nodes)

            num_zonas_contaminadas = random.randint(0,int(len(vertices)/2))

            zonas_contaminadas = set()

            while len(zonas_contaminadas) < num_zonas_contaminadas:
                zona = random.choice(vertices)
                if zona not in zonas_contaminadas:
                    zonas_contaminadas.add(zona)
            self.contaminadas = zonas_contaminadas
        self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)

    def agregar_vertice(self):
        """
        Agrega un vértice al grafo. Solicita al usuario el nombre del vértice.
        """
        if self.isModifiable:
            nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:", parent=self.root)
            if nombre and nombre not in self.G.nodes:
                self.G.add_node(nombre)
                self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
                self.asignar_zonas_contaminadas()
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
                    self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
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
    
    def bfs(self):
        """
        Encuentra la zona contaminada más cercana con un árbol de expansion (bfs).
        """
        origen = simpledialog.askstring("BFS", "Ingrese el nodo origen:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        if origen in self.G.nodes:
            arbol = bfs_amplitud(self.G,origen) # generar arbol bfs
            distancia, nodo, ruta = encontrar_mas_cercano_con_ruta(arbol,origen,self.contaminadas)
            if distancia > -1:
                self.resaltado = ruta
                messagebox.showinfo("Resultado", f"El nodo más cercano a {origen} es {nodo}, se encuentra a {distancia} nodo(s) de distancia.")
                self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
                self.roadmap.add('A11') # marcar como hecho
            else:
                messagebox.showwarning("Atención", f"No se encontro ningún nodo cercano a {origen}")
        else:
            messagebox.showerror("Error", "El nodo debe existir.")
    
    def volver(self, id):
        """
        Reiniciar la vista al volver.
        """
        self.mostrarActividad(id)
        self.resaltado = []            
        self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
    
    def volverGraficos(self,id):
        """
        Reinicia la vista al volver, reinicia tambien la vista de gráficos.
        """
        pass

    def dibujar_grafo(self,G,ax,canvas,pos,resaltado,contaminadas, optColor:str="#ff5353", optColor2: str="#ff5353"):
        """
        Dibuja el grafo en la interfaz gráfica, resaltando aristas y nodos si se proveen.
        """
        ax.clear()
        if len(contaminadas) > 0: #reduciendo procesos
            nodes_diff = set(G.nodes) - contaminadas
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#17d50c', nodelist=nodes_diff, ax=ax) # no resaltados
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color=optColor2, nodelist=contaminadas,ax=ax) # resaltados
        else:
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#17d50c', nodelist=nodes_diff,ax=ax) # no resaltados
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Montserrat", font_color='#ffffff', font_weight='bold',ax=ax) #labels de nodo

        if len(resaltado) > 0:
            edges_diff = set(G.edges) - set(resaltado)
            edge_labels_diff = {edge: G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
            edge_labels = {edge: G[edge[0]][edge[1]]["weight"] for edge in resaltado if edge in G.edges}
            nx.draw_networkx_edges(G, pos, edgelist=edges_diff, width=3, edge_color='#ffffff',ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels_diff, font_size=10, font_color='#353535', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6},ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=resaltado, edge_color=optColor, width=3)
            nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, font_color=optColor, font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.8},ax=ax)
        else:
            nx.draw_networkx_edges(G, pos, width=3, edge_color='#ffffff',ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)} , font_size=10, font_color='#353535', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6},ax=ax)

        canvas.draw()

    def on_press(self, event, pos_ref, dragging_attr):
        """Maneja el evento de presionar el mouse"""
        if event.inaxes and event.xdata is not None and event.ydata is not None:
            for node, (x, y) in pos_ref.items():
                if ((event.xdata - x)**2 + (event.ydata - y)**2) < 0.01:
                    setattr(self, dragging_attr, node)  # Usar setattr para manejar ambos dragging
                    break
                
    def on_release(self, event, dragging_attr):
        """Maneja el evento de soltar el mouse"""
        setattr(self, dragging_attr, None)  # Resetear el estado de arrastre
    
    def on_motion(self, event, pos_ref, dragging_attr, G, ax, canvas, resaltado, contaminadas):
        """Maneja el arrastre de nodos"""
        dragging = getattr(self, dragging_attr)
        if dragging and event.inaxes == ax and event.xdata is not None and event.ydata is not None:
            pos_ref[dragging] = (event.xdata, event.ydata)
            self.dibujar_grafo(G, ax, canvas, pos_ref, resaltado, contaminadas)
                    
root = ttk.Window(themename="dstheme") 

app = GuardianesBosque(root)
root.title("Guardianes del Bosque")

root.mainloop()