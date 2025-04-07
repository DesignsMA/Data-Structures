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
import numpy as np
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
        self.leerDatos()
        self._configurar_ventana()
        self._crear_ventana_bienvenida()
        self._crear_menu_frame()  # Separamos la creación del menú
        self._crear_area_grafico() # Se añade el gráfico al menu frame
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
        self.G = nx.DiGraph()
        self.H = nx.DiGraph()
        self.pos = {}
        self.secondary_pos = {}
        self.resaltado = []
        self.resaltados = []
        self.contaminadas = set()
        self.zonasRecoleccion = set()
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

Al completar todas las actividades, recibirás un
Certificado Digital como 'Guardián del Bosque'

Para completar una actividad deberás:
• Acceder a todas las actividades
• Responder cada pregunta exitosamente

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
            msgCompletado = 'Generar Certificado'
            estado = ttk.ACTIVE
        else:
            msgCompletado = 'Actividades pendientes'
            estado = ttk.DISABLED
        self.btnCertificado = ttk.Button(self.button_frame, text=msgCompletado, style=DANGER, command=self.certificar, state=estado)
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
                                                        self.resaltado, self.contaminadas, self.zonasRecoleccion))
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
                                                        self.resaltado, self.contaminadas, self.zonasRecoleccion))
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
                ("Floyd-Warshall", PRIMARY, lambda: self.validarRespuesta(22, 1, 1, 'Floyd-Warshall es ideal para encontrar todas las rutas más cortas entre todos los puntos de recolección, ahora veamos su funcionamiento!', algoritmo=self.floyd_warshall)),
                ("Siguiente ruta", PRIMARY, lambda: self.floydSiguiente()),
                ("Volver", DANGER, lambda: self.mostrarPregunta(1, 1))
            ]
        }        
        
        actividad3 = {
    "titulo": "🌿 Actividad 3: Diseño de Redes Ecológicas",
    "texto": """Objetivo:
Construir un sistema eficiente de estaciones de reciclaje con la menor cantidad de recursos. Las estaciones
de reciclaje serán ubicadas dentro de las zonas identificadas.

Métodos:

Prim: Crea un árbol abarcador mínimo comenzando desde un nodo arbitrario
Ventajas respecto a Kruskal:
  - Eficiente en grafos densos
  - Ideal para zonas con muchas rutas posibles

Kruskal: Construye el árbol agregando aristas de menor peso sin formar ciclos
Ventajas respecto a Prim:
  - Eficiente en grafos dispersos
  - Ideal para zonas con pocas rutas posibles

Criterios de Densidad:
Bosque Denso: Cuando E ≈ V(V-1)/2 (muchas conexiones posibles)
Bosque Disperso: Cuando E ≈ V-1 (solo conexiones esenciales)""",
    "botones": [
                ("Problema 1", PRIMARY, lambda: self.mostrarPregunta(2, 0, generarZonasReciclaje=True)),
                ("Problema 2", PRIMARY, lambda: self.mostrarPregunta(2, 1, generarZonasReciclaje=True)),
                ("Volver", DANGER, lambda: self.volver(2))
            ]

}

        p5 = {
            "titulo": "Bosques densos",
            "texto": """En un área con muchas conexiones posibles entre zonas (E ≈ V²):
        ¿Qué algoritmo sería más adecuado para diseñar la red de reciclaje?""",
            "botones": [
                ("Prim", PRIMARY, 
                 lambda: self.validarRespuesta(31,1,1,
                 'Correcto! Prim tiene mejor rendimiento en redes densas',
                 algoritmo=self.mst)),
                
                ("Kruskal", PRIMARY, 
                 lambda: self.validarRespuesta(31,1,0,
                 'Para esta densidad, Prim sería más eficiente')),
                
                ("Calcular Densidad", INFO, self.calcular_densidad),
                ("Volver", DANGER, lambda: self.mostrarPregunta(2,0, reiniciarGrafico=True))
            ]
        }

        p6 = {
            "titulo": "Bosques dispersos",
            "texto": """En una región con pocas conexiones entre zonas (E ≈ V):
        ¿Qué método garantiza mejor rendimiento para la red de reciclaje?""",
            "botones": [
                ("Prim", PRIMARY,
                 lambda:self.validarRespuesta(32,1,0,
                 'En redes dispersas, Kruskal es más adecuado')),
                ("Kruskal", PRIMARY,
                 lambda: self.validarRespuesta(32,1,1,
                 'Exacto! Kruskal optimiza mejor en redes con pocas conexiones',
                 algoritmo=self.mst)),
                ("Calcular Densidad", INFO, self.calcular_densidad),
                ("Volver", DANGER, lambda: self.mostrarPregunta(2,1, reiniciarGrafico=True))
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
        self.preguntas.append([crear_actividad(p5), crear_actividad(p6)]) # arreglos de preguntas
        

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
        
        self.resaltado = []
    
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
        print(self.roadmap)
        with open(ruta_archivo, "wb") as file: #escribir en binario
                # Escribir el número de elementos en el set
            file.write(len(self.roadmap).to_bytes(4, byteorder='big'))  # Guardamos el número de elementos (4 bytes)
    
            # Escribir cada entero en el set como bytes
            for elemento in self.roadmap:
                # Convertir el entero a bytes (4 bytes por entero)
                file.write(elemento.to_bytes(4, byteorder='big'))
    
    def leerDatos(self):
        ruta_archivo = os.path.join(BASE_DIR, f"Resources/data.dat")
        self.roadmap = set()
        try:
            with open(ruta_archivo, "rb") as file: #escribir en binario
                n = int.from_bytes( file.read(4), byteorder='big') # leer tamaño del set
                # Escribir cada entero en el set como bytes
                for _ in range(n):
                    self.roadmap.add( int.from_bytes(file.read(4), byteorder='big') ) #recuperar set
            print(self.roadmap)
        except FileNotFoundError:
            self.guardarDatos()

    def volver(self, id):
        """
        Reinicia la vista para volver al menú principal, limpiando los resaltados y redes.

        Esta función restablece la interfaz gráfica, mostrando el menú principal de actividades y 
        limpiando cualquier resaltado de nodos o aristas que estuviera presente en la vista anterior.

        Args:
            id (int): Identificador de la actividad a mostrar en el menú principal. 
                      Este valor determina qué actividad o pantalla será mostrada tras regresar.
        """
        preguntas = {11,12,21,22,31,32}
        if preguntas.issubset(self.roadmap): # si el usuario completo las actividades
            self.btnCertificado.configure(state=ACTIVE, text='Generar Certificado')
        self.mostrarActividad(id)
        self.resaltado = []
        self.zonasRecoleccion = set()            
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
        if not ruta:
            return

        try:
            # Combinar la ruta base con la ruta relativa
            ruta_absoluta = os.path.join(BASE_DIR, ruta)

            with open(ruta_absoluta, "r", encoding="UTF-8") as file:
                # Leer tipo de grafo
                primera_linea = file.readline().strip()
                if primera_linea not in ['True', 'False']:
                    raise ValueError("La primera línea debe ser 'True' (dirigido) o 'False' (no dirigido)")
                isDiGraph = primera_linea == 'True'

                # Leer zonas
                segunda_linea = file.readline().strip()
                if not segunda_linea:
                    raise ValueError("Falta la línea con los nombres de las zonas")
                zonas = [z.strip() for z in segunda_linea.split(',')]

                # Leer matriz de adyacencia
                matriz = []
                for i, linea in enumerate(file, start=3):  # start=3 por líneas 1 y 2 ya leídas
                    linea = linea.strip()
                    if not linea:
                        continue

                    valores = linea.split(',')
                    if len(valores) != len(zonas):
                        raise ValueError(f"Error en línea {i}: Número de columnas no coincide con el número de zonas")

                    try:
                        fila = [float(val) if val else 0.0 for val in valores]
                    except ValueError:
                        raise ValueError(f"Error en línea {i}: Valor no numérico encontrado")

                    matriz.append(fila)

            # Validaciones adicionales
            if len(matriz) != len(zonas):
                raise ValueError("La matriz de adyacencia no es cuadrada")

            # Crear grafo
            G = nx.DiGraph()
            G.add_nodes_from(zonas)

            # Añadir aristas con pesos
            for i in range(len(zonas)):
                for j in range(len(zonas)):
                    peso = matriz[i][j]

                    # Validar bucle a sí mismo
                    if i == j and peso != 0:
                        raise ValueError(f"Error en posición [{i},{j}]: No se permiten bucles (conexiones de una zona a sí misma)")

                    # Añadir arista según tipo de grafo
                    if peso != 0:
                        if isDiGraph:
                            G.add_edge(zonas[i], zonas[j], weight=peso)
                        else:
                            # Para no dirigidos, solo añadir una vez (i <= j para evitar duplicados)
                            if i <= j:
                                G.add_edge(zonas[i], zonas[j], weight=peso)
                                G.add_edge(zonas[j], zonas[i], weight=peso)

            # Asignar el grafo y calcular posiciones
            self.G = G
            self.pos = nx.spring_layout(self.G, scale=1.6, k=3/sqrt(G.number_of_nodes()))
            self.asignar_zonas_contaminadas()

            messagebox.showinfo("Éxito", "Grafo cargado correctamente")

        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {ruta}")
        except ValueError as e:
            messagebox.showerror("Error en el formato", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")
            
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
           if self.G.number_of_nodes() > 6:
               n = 3
           else:
               n = 1
           num_zonas_reciclaje = random.randint(1, n)
   
           # Creamos un conjunto para almacenar las zonas de reciclaje
           zonas_reciclaje = set()
   
           # Aseguramos que las zonas de reciclaje no sean las mismas que las zonas contaminadas
           while len(zonas_reciclaje) < num_zonas_reciclaje:
               zona = random.choice(vertices)
               if zona not in zonas_reciclaje and zona not in self.contaminadas:
                   zonas_reciclaje.add(zona)
   
           # Asignamos las zonas de reciclaje
           self.zonasRecoleccion = zonas_reciclaje
        self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)
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
                self.G.add_edge(destino, origen, weight=peso)
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
            if distancia > -1:
                self.resaltado = ruta
                messagebox.showinfo("Resultado", f"La zona más lejana a {origen} es {zona}, se encuentra a {distancia} zona(s) de distancia.")

            self.dividirPantalla(3,7)
            self.H = arbol
            self.secondary_pos = nx.spring_layout(self.H, scale=1.6, k=3/sqrt(self.H.number_of_nodes()))
            self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas)
        else:
            messagebox.showerror("Error", "La zona debe existir.")

    def dijkstra(self):
        origen = simpledialog.askstring("Dijkstra", "Ingrese alguna zona de recolección (en dorado):", parent=self.root)
        self.root.update()  # Actualizar la ventana
        if origen in self.zonasRecoleccion:
            destino = simpledialog.askstring("Dijkstra", "Ahora una zona contaminada de tu elección (en rojo):", parent=self.root)
            if destino in self.contaminadas:
                distancia, P, ruta= dijkstraFunc(self.G, origen, destino)
                self.resaltado = ruta
                if distancia is not np.inf:
                    messagebox.showinfo("Resultado", f"La zona {destino} se encuentra a {distancia} km(s) de distancia con ruta {ruta}.")
                    self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)
                    self.roadmap.add(21)
                    self.guardarDatos()
                else:
                    messagebox.showwarning("Atención", f"No se encontro ningúna zona contaminada conectada a {origen}, intenta con otra")
            else:
                messagebox.showwarning("Atención", f"No se encontro ningúna zona contaminada de nombre {destino}")
        else:
            messagebox.showerror("Error", "La zona debe ser una zona de recolección.")
    
    def floyd_warshall(self):
        self.root.update()  # Actualizar la ventana
        resultado = encontrar_rutas_contaminadas_reciclaje(self.G,self.contaminadas, self.zonasRecoleccion) # retorna todas las rutas más cortas de cada centro a cada zona contaminada
        msg = ""
        self.resaltados = []
        for origen, destino, ruta, costo in resultado:
            msg	+= f"{origen} -> {destino} | {costo} km(s) de distancia con ruta {ruta}\n."
            self.resaltados.append(ruta)
        messagebox.showinfo("Rutas Resultantes", msg)
        self.floydSiguiente()
        self.roadmap.add(22)
        self.guardarDatos()

    def floydSiguiente(self):
        if len(self.resaltados) > 0:
            self.resaltado = self.resaltados.pop()
            self.dibujar_grafo(self.G,self.ax,self.canvas,self.pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)
        else:
            messagebox.showinfo(message="Ya visualizó todos los caminos.")

    def kruskal(self):
        G = nx.Graph(self.G)
            
        if nx.is_connected(G):  # Si el grafo es conexo y no dirigido
            self.secondary_canvas.draw()
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
            start = list(self.zonasRecoleccion)[0]
            self.H = MST
            self.secondary_pos = self.generar_posiciones_arbol(self.G, start)
            messagebox.showinfo("Kruskal", "Proceso comenzado.")
            def agregar_arista_a_MST():
                if len(A) > 0:
                    u, v, weight = A.pop(0)  # Obtener la arista con el menor peso
                    self.resaltado = [(u,v)]  # Resaltar las aristas del MST
                    if ENCUENTRA(u) != ENCUENTRA(v):  # Si no forman un ciclo
                        self.H.add_edge(u, v, **weight)  # Añadir la arista al MST
                        COMBINA(u, v)  # Combinar las componentes
                        # Actualizar visualización
                        self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)
                        self.root.after(500, agregar_arista_a_MST)
                    else:
                            # Llamar a la función de nuevo después de 500 ms
                        self.root.after(500, agregar_arista_a_MST)
                else:
                    # Cuando todas las aristas han sido procesadas
                    messagebox.showinfo("Proceso completado", "El árbol de expansión mínima ha sido encontrado.")
                    self.resaltado = list(self.G.edges)
                    self.secondary_pos = self.generar_posiciones_arbol(self.H, start)
                    self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)
            # Iniciar el proceso de construcción del MST
            if len(A) > 0 :
                agregar_arista_a_MST()
        else:
            messagebox.showerror(message="El grafo debe ser no dirigido y conexo.")

    def prim_mst(self):
        start = simpledialog.askstring("Introduzca lo pedido", "Ingrese la zona de recoleccíon desde donde creara la red:", parent=self.root)
        self.root.update()  # Actualizar la ventana

        G = self.G
        
        if start not in self.zonasRecoleccion:
            messagebox.showerror(message="No es una zona de recolección valida.")
            return

        self.secondary_canvas.draw()
        U = {start}  # Conjunto de nodos en el MST
        Tree = nx.Graph()  # Grafo resultante para el árbol de expansión mínima
        aristas_candidatas = []
        self.H = Tree
        self.secondary_pos = self.generar_posiciones_arbol(self.G, start)
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
                self.H.add_edge(nodo1, nodo2, weight=peso)
                self.resaltado = [(nodo1, nodo2)]  # Para resaltar la arista en la interfaz
                self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)

                U.add(nodo2)  # Agregar el nodo al conjunto U

                # Llamar de nuevo después de 1 segundo para la siguiente iteración
                self.root.after(500, actualizar_arista)
                
            else:
                messagebox.showinfo("Proceso completado", "El árbol de expansión mínima ha sido encontrado.")
                self.resaltado = list(Tree.edges)
                self.secondary_pos = self.generar_posiciones_arbol(self.H, start)
                self.dibujar_grafo(self.H,self.secondary_ax,self.secondary_canvas,self.secondary_pos,self.resaltado,self.contaminadas, optColor2='#e59b06', resaltado2=self.zonasRecoleccion)

        # Iniciar el proceso de encontrar el MST
        actualizar_arista()
    
    def calcular_densidad(self):
        """
        Calcula la densidad del grafo y recomienda el algoritmo óptimo
        Densidad = Número de aristas actuales / Máximo número posible de aristas
        """
        if not hasattr(self, 'G') or self.G.number_of_nodes() == 0:
            messagebox.showerror("Error", "Primero debe cargar un grafo")
            return

        V = self.G.number_of_nodes()
        E = self.G.number_of_edges()

        # Para grafos no dirigidos
        max_edges = V * (V - 1) / 2 if not self.G.is_directed() else V * (V - 1)
        min_edges = V - 1  # Mínimo para grafo conexo

        densidad = E / max_edges if max_edges > 0 else 0

        # Determinar recomendación
        if densidad > 0.5:
            recomendacion = "PRIM"
        elif densidad < 0.3:
            recomendacion = "KRUSKAL"
        else:
            recomendacion = "COMPARAR"

        # Mostrar resultados
        resultado = (
            f"● Número de nodos (V): {V}\n"
            f"● Número de aristas (E): {E}\n"
            f"● Aristas mínimas requeridas: {min_edges}\n"
            f"● Aristas máximas posibles: {int(max_edges)}\n"
            f"● Densidad del grafo: {densidad:.2%}\n\n"
            f"RECOMENDACIÓN: {recomendacion}"
        )

        messagebox.showinfo(
            "Análisis de Densidad", 
            resultado
        )
        
        return recomendacion

    
    def mst(self):
        algoritmo = simpledialog.askstring("Introduzca el algoritmo", "Prim | Kruskal | Densidad", parent=self.root)
        if algoritmo:
            self.dividirPantalla(3,7)
            if algoritmo.lower() == 'prim':
                self.prim_mst() 
            elif algoritmo.lower() == 'kruskal':
                self.kruskal() 
            else:
                algoritmo = self.calcular_densidad()   
                if algoritmo == 'PRIM':
                    self.prim_mst()       
                else:
                    self.kruskal()  
    
    def certificar(self):
        nombre = simpledialog.askstring("Introduzca su nombre", "Nombre del participante: ", parent=self.root)
        path = os.path.join(BASE_DIR,'Certificado.png')
        if nombre:
            nombre = nombre.capitalize()
            crear_certificado(nombre, path)
            messagebox.showinfo(message=f"Su certificado se encuentra en {path}, felicidades {nombre}!")
        

    def dividirPantalla(self, ancho, alto):
        self.fig.set_size_inches(ancho, alto)  # Nuevo tamaño en pulgadas (ancho, alto)
        self.canvas.draw()  # Esto fuerza el redibujado
        self.canvas.get_tk_widget().config(width=int(ancho*self.fig.dpi), height=int(7*self.fig.dpi))
        if not self.secondary_graph.winfo_ismapped():
            self.toggle_mostrar_ocultar(self.secondary_graph) # mostrar pero no ocultar

        
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

    def dibujar_grafo(self, G, ax, canvas, pos, resaltado=None, contaminadas=None, optColor: str = "#ff5353", optColor2: str = "#ff5353", resaltado2: list = None):
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

        # Validar parámetros opcionales
        resaltado = resaltado or []
        contaminadas = contaminadas or set()
        resaltado2 = resaltado2 or []

        # Dibujar nodos
        all_nodes = set(G.nodes())
        clean_nodes = all_nodes - contaminadas

        # Dibujar nodos no contaminados
        if clean_nodes:
            nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#17d50c', 
                                  nodelist=list(clean_nodes), ax=ax)

        # Dibujar nodos contaminados
        if contaminadas:
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color=optColor, 
                                  nodelist=list(contaminadas), ax=ax)

        # Dibujar segundo conjunto de nodos resaltados
        if resaltado2:
            valid_resaltado2 = [n for n in resaltado2 if n in all_nodes]
            nx.draw_networkx_nodes(G, pos, node_size=500, node_color=optColor2, 
                                  nodelist=valid_resaltado2, ax=ax)

        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="Montserrat", 
                               font_color='#ffffff', font_weight='bold', ax=ax)

        # Manejo seguro de aristas
        all_edges = set(G.edges())

        # Filtrar aristas resaltadas que existen en el grafo
        valid_resaltado = [e for e in resaltado if e in all_edges or (e[1], e[0]) in all_edges]

        # Dibujar aristas no resaltadas
        if resaltado:
            edges_diff = all_edges - set(valid_resaltado)
        else:
            edges_diff = all_edges

        # Dibujar todas las aristas base
        nx.draw_networkx_edges(G, pos, edgelist=list(all_edges), width=3, 
                              edge_color='#ffffff', ax=ax, arrows=False)

        # Dibujar etiquetas de aristas
        edge_labels = {}
        for u, v, d in G.edges(data=True):
            edge_labels[(u, v)] = d.get('weight', '')

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, 
                                   font_color='#353535', font_family="Montserrat", 
                                   font_weight='bold', 
                                   bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), 
                                   "fc": (1.0, 1.0, 1.0), "alpha": 0.6}, ax=ax)

        # Dibujar aristas resaltadas si existen
        if valid_resaltado:
            # Para grafos no dirigidos, verificar ambas direcciones
            actual_resaltado = []
            for e in valid_resaltado:
                if e in all_edges:
                    actual_resaltado.append(e)
                elif (e[1], e[0]) in all_edges:
                    actual_resaltado.append((e[1], e[0]))

            nx.draw_networkx_edges(G, pos, edgelist=actual_resaltado, 
                                  edge_color=optColor, width=5, ax=ax, arrows=False)

            # Resaltar etiquetas de aristas resaltadas
            resaltado_labels = {e: G[e[0]][e[1]]['weight'] for e in actual_resaltado}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=resaltado_labels, 
                                        font_size=10, font_color=optColor, 
                                        font_family="Montserrat", font_weight='bold', 
                                        bbox={"boxstyle": "round", "ec": (1.0, 1.0, 1.0), 
                                        "fc": (1.0, 1.0, 1.0), "alpha": 0.8}, ax=ax)

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