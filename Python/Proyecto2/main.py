import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime
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
        self._inicializar_grafo()
        self._configurar_ventana()
        self._crear_ventana_bienvenida()
        self._crear_menu_frame()  # Separamos la creación del menú
        self._crear_area_grafico() # Se añade el gráfico al menu frame
        self._definirActividades()
        self.menu_frame.grid_remove()
        self.leerDatos()
        
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
        self.zonasReciclaje = set()
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
        messagebox.showinfo(message="En esta pantalla podrá editar y cargar un grafo que representa la zona de bosques que debemos proteger, tambien serán asignadas zonas contaminadas aleatorias, sin embargo puede generar nuevas presionando el botón.")
        
        
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
        
        preguntas = {11,12,21,22,31,32}
        if preguntas.issubset(self.roadmap):
            msgCompletado = 'Generar certificado'
            estado = ttk.ACTIVE
        else:
            msgCompletado = 'Actividades pendientes'
            estado = ttk.DISABLED
        self.btnCertificado = ttk.Button(self.button_frame, text=msgCompletado, style=DANGER, command=self.root.quit, state=estado)
        self.btnCertificado.grid(row=i+1,sticky='ew', pady=30)
        self.funcionesBtn.append(self.btnCertificado)
        
    
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
                                                        self.resaltado, self.contaminadas, self.zonasReciclaje))
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
                                                        self.resaltado, self.contaminadas, self.zonasReciclaje))
                self.secondary_fig, self.secondary_ax, self.secondary_canvas = fig, ax, canvas
                self.secondary_dragging = None  # Estado de arrastre para figura secundaria            
    def _definirActividades(self):
                # Definición de actividades
        self.actividades = []
        self.preguntas = [] # lista de widgets para una pregunta

        # Actividad 1
        actividad1 = {
            "titulo":"""🔍 Actividad 1: Exploración de Ecosistemas""",

            "texto": """Objetivo: Identificar y recorrer eficientemente alguna zona contaminada para planificar la recolección de residuos.

Algoritmos:

BFS (Breadth-First Search - Recorrido en Anchura)
El BFS explora un grafo por nivel, comenzando desde un punto inicial y expandiéndose a todos los vecinos inmediatos antes de avanzar a zonas más lejanos. Utiliza una cola para garantizar que los zonas se visiten en orden de proximidad, lo que asegura que siempre encuentre la solución más cercana primero. Es eficiente en espacios donde la distancia o el tiempo de acceso son críticos.

DFS (Depth-First Search - Recorrido en Profundidad)
El DFS recorre un grafo o matriz avanzando lo más posible por una rama antes de retroceder y probar caminos alternativos. Usa una pila (o recursión) para profundizar en una dirección hasta agotar las opciones, lo que lo hace útil para explorar estructuras complejas o laberínticas. A diferencia del BFS, no garantiza encontrar la solución más cercana, pero puede descubrir rutas menos evidentes o patrones ocultos.""",
            "botones": [
                ("Problema 1", PRIMARY, lambda: self.mostrarPregunta(0,0)),
                ("Problema 2", PRIMARY, lambda: self.mostrarPregunta(0,1)),
                ("Volver", DANGER, lambda: self.volver(0))
            ]
        }
        
        p1 = {
            "titulo":"""¿Cúal sería el algoritmo más apropiado para encontrar la zona contaminada más cercana a otra considerando solo las conexiones?""",

            "texto": """...""",
            "botones": [
                ("BFS", PRIMARY, lambda: self.validarRespuesta(11,1,1,'BFS es ideal para encontrar la zona contaminada más cercana, ahora realizemos un ejemplo!',algoritmo=self.bfs)),
                ("DFS", PRIMARY, lambda: self.validarRespuesta(11,1,0)),
                ("Volver", DANGER, lambda: self.mostrarPregunta(0,0))
            ]
        }
        
        p2 = {
            "titulo":"""¿Cúal sería el algoritmo más apropiado para explorar a fondo cada zona y con esto detectar problemas más extensos?""",

            "texto": """...""",
            "botones": [
                ("BFS", PRIMARY, lambda:self.validarRespuesta(12,1,0)),
                ("DFS", PRIMARY, lambda: self.validarRespuesta(12,1,1,'DFS es ideal para identificar problemas más extensos, ahora realizemos un ejemplo!',algoritmo=self.dfs)),
                ("Volver", DANGER, lambda: self.mostrarPregunta(0,1, True))
            ]
        }

        actividad2 = {
            "titulo": """🔍 Actividad 2: Optimización de rutas de recolección""",
            "texto": """Objetivo:
        Determinar la mejor ruta para transportar residuos a los centros de reciclaje con el menor costo posible.
        Los camiones o recolectores siguen estas rutas optimizadas para minimizar costos de transporte.

        Métodos:

        Dijkstra: Encuentra la ruta más corta desde un punto específico. Encuentra la zona contaminada más cercana desde un punto inicial, útil si la contaminación es dispersa.

        Floyd-Warshall: Encuentra las rutas más cortas entre todas las estaciones de recolección. Es útil si hay varias zonas contaminadas conectadas entre sí, ya que permite encontrar las rutas más cortas entre todos los puntos de recolección."""
            ,
            "botones": [
                ("Problema 1", PRIMARY, lambda: self.mostrarPregunta(1, 0, generarZonasReciclaje=True)),
                ("Problema 2", PRIMARY, lambda: self.mostrarPregunta(1, 1, generarZonasReciclaje=True)),
                ("Volver", DANGER, lambda: self.volver(1))
            ]
        }

        # Pregunta 1
        p3 = {
            "titulo": """¿Qué algoritmo sería el más adecuado para encontrar la ruta más corta desde un punto específico a otro para una recolección eficiente?""",
            "texto": """Dado un mapa de rutas y un punto inicial, necesitas encontrar la ruta más corta hacia un destino específico para optimizar el proceso de recolección. Este algoritmo debe ser capaz de evaluar el costo de las rutas de manera eficiente."""
            ,
            "botones": [
                ("Dijkstra", PRIMARY, lambda: self.validarRespuesta(21, 1, 1, 'Dijkstra es ideal para encontrar la ruta más corta desde un punto inicial, ahora realizemos un ejemplo!', algoritmo=self.dijkstra)),
                ("Floyd-Warshall", PRIMARY, lambda: self.validarRespuesta(21, 1, 0)),
                ("Volver", DANGER, lambda: self.mostrarPregunta(1, 0))
            ]
        }

        # Pregunta 2
        p4 = {
            "titulo": """¿Qué algoritmo sería el más adecuado si necesitamos encontrar todas las rutas más cortas entre todas las estaciones de recolección?""",
            "texto": """En este caso, necesitas conocer las rutas más cortas entre todas las estaciones de recolección. Este algoritmo será útil cuando existan múltiples puntos de recolección y desees optimizar el transporte entre todos los puntos.""" 
            ,
            "botones": [
                ("Dijkstra", PRIMARY, lambda: self.validarRespuesta(22, 1, 0)),
                ("Floyd-Warshall", PRIMARY, lambda: self.validarRespuesta(22, 1, 1, 'Floyd-Warshall es ideal para encontrar todas las rutas más cortas entre todos los puntos de recolección, ahora realizemos un ejemplo!', algoritmo=self.floyd_warshall)),
                ("Volver", DANGER, lambda: self.mostrarPregunta(1, 1))
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
                font=("Montserrat Bold", 12),
                justify="center",
                wraplength=400,
                padding=2
            )
            ttl.grid(row=row_start, pady=3)
            widgets.append(ttl)
            lbl = ttk.Label(
                master=self.button_frame,
                text=actividad["texto"],
                font=("Montserrat Light", 10),
                justify="left",
                wraplength=400,
            )
            lbl.grid(row=row_start+1, pady=10)
            widgets.append(lbl)

            # Crear botones principales
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
        self.preguntas.append([crear_actividad(p1), crear_actividad(p2)]) # arreglos de preguntas
        self.actividades.append(crear_actividad(actividad2))
        self.preguntas.append([crear_actividad(p3), crear_actividad(p4)]) # arreglos de preguntas
        self.actividades.append(crear_actividad(actividad3))
        

        # Ocultar todas las actividades inicialmente
        for actividad in self.actividades:
            for widget in actividad:
                widget.grid_remove()

        for preguntas in self.preguntas: # ocultar preguntas
            for pregunta in preguntas:
                for widget in pregunta:
                    widget.grid_remove()

    def mostrarActividad(self, id):
        for btn in self.funcionesBtn:
            self.toggle_mostrar_ocultar(btn) # ocultar o mostrar botones
        
        for widget in self.actividades[id]:
            self.toggle_mostrar_ocultar(widget)
    
    def mostrarPregunta(self, idActividad, idPregunta, reiniciarGrafico: bool = False, generarZonasReciclaje: bool = False):
        for widget in self.actividades[idActividad]: # mostrar u ocultar actividad
            self.toggle_mostrar_ocultar(widget)
            
        for widget in self.preguntas[idActividad][idPregunta]: # mostrar pregunta idPregunta de la actividad idActividad
            self.toggle_mostrar_ocultar(widget)
        
        if reiniciarGrafico:
            self.reiniciarGraficos()
        
        if generarZonasReciclaje:
            self.asignar_zonas_reciclaje()
    
    def validarRespuesta(self, id,correcta: int, respuesta: int, 
                        msgCorrecto: str = 'Tu respuesta es correcta', msgIncorrecto: str = 'Tu respuesta es incorrecta!', 
                        algoritmo=None, *args):
        """
        Valida si una respuesta es correcta y ejecuta una función callback si lo es.

        Args:
            correcta (int): Respuesta correcta esperada
            respuesta (int): Respuesta proporcionada por el usuario
            msgCorrecto (str): Mensaje a mostrar si es correcto
            msgIncorrecto (str): Mensaje a mostrar si es incorrecto
            algoritmo (callable, optional): Función a ejecutar si es correcto
            *args: Argumentos adicionales para la función algoritmo
        """
        if self.G.number_of_edges() > 0:
            if respuesta == correcta:
                messagebox.showinfo("Correcto!", msgCorrecto)
                self.roadmap.add(id)
                self.guardarDatos()
                if algoritmo:  # Verifica que se haya proporcionado un algoritmo
                    algoritmo(*args)  # Desempaqueta los argumentos
            else:
                messagebox.showinfo("Incorrecto", msgIncorrecto)
        else:
            messagebox.showinfo(message="Carga al menos una zona conectada con otra para continuar.")
    
    def guardarDatos(self):
        ruta_archivo = os.path.join(BASE_DIR, f"Resources/data.dat")
        # Asegurarse de que el directorio exista
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        with open(ruta_archivo, "wb") as file: #escribir en binario
                # Escribir el número de elementos en el set
            file.write(len(self.roadmap).to_bytes(4, byteorder='big'))  # Guardamos el número de elementos (4 bytes)
    
            # Escribir cada entero en el set como bytes
            for elemento in self.roadmap:
                # Convertir el entero a bytes (4 bytes por entero)
                file.write(elemento.to_bytes(4, byteorder='big'))
    
    def leerDatos(self):
        ruta_archivo = os.path.join(BASE_DIR, f"Resources/data.dat")
        with open(ruta_archivo, "rb") as file: #escribir en binario
            n = int.from_bytes( file.read(4), byteorder='big') # leer tamaño del set
            # Escribir cada entero en el set como bytes
            for _ in range(n):
                self.roadmap.add( int.from_bytes(file.read(4), byteorder='big') ) #recuperar set

    def volver(self, id):
        """
        Reinicia la vista para volver al menú principal, limpiando los resaltados y redes.

        Esta función restablece la interfaz gráfica, mostrando el menú principal de actividades y 
        limpiando cualquier resaltado de nodos o aristas que estuviera presente en la vista anterior.

        Args:
            id (int): Identificador de la actividad a mostrar en el menú principal. 
                      Este valor determina qué actividad o pantalla será mostrada tras regresar.
        """
        self.mostrarActividad(id)
        self.resaltado = []
        self.zonasReciclaje = set()            
        self.dibujar_grafo(self.G, self.ax, self.canvas, self.pos, self.resaltado, self.contaminadas)
            
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

                    # Leer zonas
                    segunda_linea = file.readline().strip()
                    if not segunda_linea:
                        raise ValueError("Falta la línea de nombres de zonas")
                    zonas = segunda_linea.split(',')

                    # Leer matriz de adyacencia
                    matriz = []
                    for i, linea in enumerate(file):
                        valores = linea.strip().split(',')
                        if len(valores) != len(zonas):
                            raise ValueError(f"La fila {i+3} no tiene el número correcto de columnas")
                        try:
                            fila = [float(val) if val else 0.0 for val in valores]
                        except ValueError:
                            raise ValueError(f"Valor no numérico en la fila {i+3}")
                        matriz.append(fila)

                    # Verificar matriz cuadrada
                    if len(matriz) != len(zonas):
                        raise ValueError("La matriz de adyacencia no es cuadrada")

                    # Crear grafo
                    G = nx.DiGraph() if isDiGraph else nx.Graph()
                    G.add_nodes_from(zonas)

                    # Añadir aristas con pesos
                    for i in range(len(zonas)):
                        for j in range(len(zonas)):
                            peso = matriz[i][j]
                            if peso != 0:
                                if isDiGraph or (not isDiGraph and i <= j):
                                    if zonas[i] == zonas[j]:
                                        raise ValueError(f"Columna {i} | Fila {j}\nNo puede haber una ruta a si mismo.")
                                    G.add_edge(zonas[i], zonas[j], weight=peso)

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
        if self.G.number_of_nodes() > 2:
            grafo = self.G
            vertices = list(grafo.nodes)

            num_zonas_contaminadas = random.randint(1,int(len(vertices)/2))

            zonas_contaminadas = set()

            while len(zonas_contaminadas) < num_zonas_contaminadas:
                zona = random.choice(vertices)
                if zona not in zonas_contaminadas:
                    zonas_contaminadas.add(zona)
            self.contaminadas = zonas_contaminadas
        self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)

    def asignar_zonas_reciclaje(self):
        if self.G.number_of_nodes() > 2:
           grafo = self.G
           vertices = list(grafo.nodes)
   
           # Determinamos un número aleatorio de zonas de reciclaje (por ejemplo, hasta la mitad del número de nodos)
           num_zonas_reciclaje = random.randint(1, int(len(vertices) / 2))
   
           # Creamos un conjunto para almacenar las zonas de reciclaje
           zonas_reciclaje = set()
   
           # Aseguramos que las zonas de reciclaje no sean las mismas que las zonas contaminadas
           while len(zonas_reciclaje) < num_zonas_reciclaje:
               zona = random.choice(vertices)
               if zona not in zonas_reciclaje and zona not in self.contaminadas:
                   zonas_reciclaje.add(zona)
   
           # Asignamos las zonas de reciclaje
           self.zonasReciclaje = zonas_reciclaje
        self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasReciclaje)
    def agregar_vertice(self):
        """
        Agrega un vértice al grafo. Solicita al usuario el nombre del vértice.
        """
        nombre = simpledialog.askstring("Agregar Zona", "Ingrese el nombre de la zona:", parent=self.root)
        if nombre and nombre not in self.G.nodes:
            self.G.add_node(nombre)
            self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
            self.asignar_zonas_contaminadas()
        elif nombre in self.G.nodes:
            messagebox.showerror(message="Ya existe esa zona.")

    def agregar_arista(self):
        """
        Agrega una arista al grafo. Solicita al usuario el zona origen, zona destino y peso de la arista.
        """
        origen = simpledialog.askstring("Agregar Ruta", "Ingrese la zona origen:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        destino = simpledialog.askstring("Agregar Ruta", "Ingrese la zona destino:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        peso = simpledialog.askfloat("Agregar Ruta", "Ingrese la distancia en km:", parent=self.root)
        if origen in self.G.nodes and destino in self.G.nodes and peso:
            if origen == destino:
                messagebox.showerror("Error", "No puede haber una ruta a si mismo.")
                return
            if peso >= 0:
                self.G.add_edge(origen, destino, weight=peso)
                self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
            else:
                messagebox.showerror("Error", "La distancia debe ser válida (0-Inf).")
        else:
            messagebox.showerror("Error", "Las zonas deben existir y la distancia debe ser válida (0-Inf).")
    
    def generar_posiciones_arbol(self,G: nx.Graph, root):
        niveles = {}  # Diccionario para almacenar niveles de cada zona
        posiciones = {}  # Diccionario de posiciones finales
        visitados = set()  # Para evitar ciclos

        # Obtener estructura de árbol (suponiendo que G es un árbol o un MST)
        arbol = nx.bfs_tree(G, root)  # Usa búsqueda en anchura (BFS) para formar un árbol desde root

        def dfs(zona, nivel=0, x=0, ancho=1):
            if zona in visitados:
                return
            visitados.add(zona)
            niveles[zona] = nivel
            posiciones[zona] = (x, -nivel)  # -nivel para que crezca hacia abajo

            hijos = list(arbol[zona])  # Solo tomamos los hijos en el árbol BFS
            num_hijos = len(hijos)

            for i, hijo in enumerate(hijos):
                dfs(hijo, nivel + 1, x + (i - (num_hijos - 1) / 2) * ancho / 2, ancho / 2)

        dfs(root)
        return posiciones            
    
    def bfs(self):
        """
        Encuentra la zona contaminada más cercana con un árbol de expansion (bfs).
        """
        origen = simpledialog.askstring("BFS", "Ingrese la zona origen:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        if origen in self.G.nodes:
            arbol = bfs_amplitud(self.G,origen) # generar arbol bfs
            distancia, zona, ruta = encontrar_mas_cercano_con_ruta(arbol,origen,self.contaminadas)
            if distancia > -1:
                self.resaltado = ruta
                messagebox.showinfo("Resultado", f"La zona más cercana a {origen} es {zona}, se encuentra a {distancia} zona(s) de distancia.")
                self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
            else:
                messagebox.showwarning("Atención", f"No se encontro ningúna zona cercana a {origen}")
        else:
            messagebox.showerror("Error", "La zona debe existir.")
    
    def dfs(self):
        """
        Encuentra el arbol de expansión a profundidad por medio de dfs.
        """
        origen = simpledialog.askstring("DFS", "Ingrese la zona origen:", parent=self.root)
        self.root.update()  # Actualizar la ventana
        if origen in self.G.nodes:
            arbol = nx.Graph()
            aristas_con_pesos = dfs_profundidad(self.G,origen) # generar arbol dfs
            for (u, v, peso) in aristas_con_pesos:
                arbol.add_edge(u, v, weight=peso)  # Añade la arista con su peso
            distancia, zona, ruta = encontrar_mas_lejano_con_ruta(arbol,origen,self.contaminadas)
            print(ruta)
            if distancia > -1:
                self.resaltado = ruta
                messagebox.showinfo("Resultado", f"La zona más lejana a {origen} es {zona}, se encuentra a {distancia} zona(s) de distancia.")

            self.dividirPantalla(arbol,origen,3,7, layout='spring')
        else:
            messagebox.showerror("Error", "La zona debe existir.")

    def dijkstra(self):
        origen = simpledialog.askstring("Dijkstra", "Ingrese alguna zona de recolección (en dorado):", parent=self.root)
        self.root.update()  # Actualizar la ventana
        if origen in list(self.zonasReciclaje):
            D, P, ruta = dijkstraFunc(self.G, origen, )
            distancia, zona, ruta = encontrar_mas_cercano_con_ruta(arbol,origen,self.contaminadas)
            if distancia > -1:
                self.resaltado = ruta
                messagebox.showinfo("Resultado", f"La zona más cercana a {origen} es {zona}, se encuentra a {distancia} zona(s) de distancia.")
                self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas)
            else:
                messagebox.showwarning("Atención", f"No se encontro ningúna zona cercana a {origen}")
        else:
            messagebox.showerror("Error", "La zona debe ser una zona de reciclaje.")

        
    def dividirPantalla(self, H: nx.DiGraph, origen, ancho: int = 5, alto: int = 7, layout: str = 'tree'):
        self.fig.set_size_inches(ancho, alto)  # Nuevo tamaño en pulgadas (ancho, alto)
        self.canvas.draw()  # Esto fuerza el redibujado
        self.canvas.get_tk_widget().config(width=int(ancho*self.fig.dpi), height=int(7*self.fig.dpi))
        self.toggle_mostrar_ocultar(self.secondary_graph)
        self.H = H
        if layout == 'tree':
            self.secondary_pos = self.generar_posiciones_arbol(self.H,origen)
        else:
            self.secondary_pos = nx.spring_layout(self.H, scale=1, k=3/sqrt(self.H.number_of_nodes()))
            
        self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas)

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

        
    def reiniciarGraficos(self):
        """
        Reinicia la vista de gráficos.
        
        """
        self.fig.set_size_inches(10, 7)  # Nuevo tamaño en pulgadas (ancho, alto)
        self.canvas.draw()  # Esto fuerza el redibujado
        self.canvas.get_tk_widget().config(width=int(10*self.fig.dpi), height=int(7*self.fig.dpi))
        self.toggle_mostrar_ocultar(self.secondary_graph)
        self.H =  None
        self.secondary_pos = {}
        self.secondary_ax.clear()
        self.secondary_canvas.draw()

    def dibujar_grafo(self, G, ax, canvas, pos, resaltado, contaminadas, optColor: str = "#ff5353", optColor2: str = "#ff5353", resaltado2: list = None):
        """
        Dibuja el grafo en la interfaz gráfica, resaltando aristas y nodos si se proveen.
        Además, permite resaltar un segundo conjunto de nodos y optimiza los procesos de dibujo.

        Args:
            G: Grafo.
            ax: Eje donde se dibuja el grafo.
            canvas: Lienzo para el dibujo.
            pos: Posiciones de los nodos.
            resaltado: Lista de aristas a resaltar.
            contaminadas: Lista de nodos a resaltar como contaminadas.
            optColor: Color para los nodos resaltados (por defecto rojo).
            optColor2: Color para el segundo conjunto de nodos resaltados.
            resaltado2: Lista de nodos a resaltar (opcional, segundo conjunto de nodos).
        """
        ax.clear()

        # Optimización: Procesar nodos no contaminados y contaminados solo una vez
        if contaminadas:
            nodes_diff = set(G.nodes) - contaminadas
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#17d50c', nodelist=nodes_diff, ax=ax)  # No resaltados
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color=optColor2, nodelist=contaminadas, ax=ax)  # Resaltados
        else:
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#17d50c', nodelist=set(G.nodes), ax=ax)  # No resaltados

        # Resaltar el segundo conjunto de nodos si se proporciona
        if resaltado2:
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color=optColor, nodelist=resaltado2, ax=ax)  # Segundo resaltado

        # Dibujar las etiquetas de los nodos
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Montserrat", font_color='#ffffff', font_weight='bold', ax=ax)

        # Dibujar aristas
        if resaltado:
            edges_diff = set(G.edges) - set(resaltado)
            edge_labels_diff = {edge: G[edge[0]][edge[1]]["weight"] for edge in edges_diff}
            edge_labels = {edge: G[edge[0]][edge[1]]["weight"] for edge in resaltado}

            # Dibujar las aristas no resaltadas
            nx.draw_networkx_edges(G, pos, edgelist=edges_diff, width=3, edge_color='#ffffff', ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels_diff, font_size=10, font_color='#353535', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6}, ax=ax)

            # Dibujar las aristas resaltadas
            nx.draw_networkx_edges(G, pos, edgelist=resaltado, edge_color=optColor, width=3, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, font_color=optColor, font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.8}, ax=ax)
        else:
            # Dibujar todas las aristas si no se resalta ninguna
            nx.draw_networkx_edges(G, pos, width=3, edge_color='#ffffff', ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)}, font_size=10, font_color='#353535', font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0), "alpha": 0.6}, ax=ax)

        # Actualizar el lienzo
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
    
    def on_motion(self, event, pos_ref, dragging_attr, G, ax, canvas, resaltado, contaminadas, reciclaje):
        """Maneja el arrastre de zonas"""
        dragging = getattr(self, dragging_attr)
        if dragging and event.inaxes == ax and event.xdata is not None and event.ydata is not None:
            pos_ref[dragging] = (event.xdata, event.ydata)
            self.dibujar_grafo(G, ax, canvas, pos_ref, resaltado, contaminadas, optColor2='#e59b06', resaltado2=reciclaje)
                    
root = ttk.Window(themename="dstheme") 

app = GuardianesBosque(root)
root.title("Guardianes del Bosque")

root.mainloop()