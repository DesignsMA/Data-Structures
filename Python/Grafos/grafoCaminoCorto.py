import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GrafoInteractivo:
    def __init__(self, root: tk.Tk):
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
        tk.Button(self.menu_frame, text="Floyd Marshall", command=self.floyd).pack(fill=tk.X, pady=5)
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
        self.pos = {}
        self.camino = []
        self.caminos = []

        # Habilitar movimiento de nodos
        self.dragging = None
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def agregar_vertice(self):
        nombre = simpledialog.askstring("Agregar Vértice", "Ingrese el nombre del vértice:", parent=self.root)
        if nombre and nombre not in self.G.nodes:
            self.G.add_node(nombre)
            self.pos[nombre] = (len(self.G.nodes), len(self.G.nodes))  # Posición inicial
            self.dibujar_grafo()

    def agregar_arista(self):
        origen = simpledialog.askstring("Agregar Arista", "Ingrese el nodo origen:", parent=self.root)
        root.update()  # Actualizar la ventana
        destino = simpledialog.askstring("Agregar Arista", "Ingrese el nodo destino:", parent=self.root)
        root.update()  # Actualizar la ventana
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
        self.ax.clear()
        self.camino = []
        self.dibujar_grafo()
        
    def dijkstraFunc(self, origen):
    # Número de nodos
        n = self.G.number_of_nodes()

        # Lista de nodos para mapear índices
        V = list(self.G.nodes)

        # Matriz de costos
        C = np.full((n,n), np.inf)
        for a,b in self.G.edges: # por cada par de vertices que definen a un arista
            C[V.index(a), V.index(b)] = self.G.adj[a][b]['weight'] # en la posición correspondiente a la matriz, asignar el peso de ir de a a b           
            
        print("Matriz de costos:\n", C)

        # Inicialización de S, D y P
        S = set([origen])  # S inicia con el origen (usando un conjunto)
        D = {}  # Diccionario de distancias
        P = {}  # Diccionario de predecesores

        # Inicializando distancias
        for i in range(n):
            if V[i] == origen:  # El nodo de origen tiene distancia 0
                D[V[i]] = 0
            else:
                if (origen, V[i]) in self.G.edges:  # Si hay conexión
                    D[V[i]] = C[V.index(origen), i]
                else:  # Si no hay conexión
                    D[V[i]] = np.inf

        # Bucle principal
        Predecesores = {v: {} for v in V} # diccionario de predecesores
        for _ in range(n-1):
            P = {}  #reiniciando p
            # Elige un vértice w en V-S tal que D[w] es mínimo
            w = min((v for v in V if v not in S), key=lambda v: D[v])

            # Agrega w a S
            S.add(w)

            # Actualiza las distancias de los vecinos de w
            for v in V:
                print(P)
                if v not in S and C[V.index(w), V.index(v)] != np.inf:
                    print(V[V.index(w)])
                    print(V[V.index(v)])
                    if D[w] + C[V.index(w), V.index(v)] < D[v]:
                        P[v] = w  # Añadir predecesor si pasando por w, mejora camino
                        D[v] = D[w] + C[V.index(w), V.index(v)]
                        Predecesores[ V[V.index(v)] ] = P #  actualizar lista de predecesores de v
            
        return D, Predecesores

    def floydFunc(self):
                # Crear matriz de adyacencia inicializada con infinitos
        G = self.G
        n = G.number_of_nodes()
        nodos = list(G.nodes)  # Lista de nodos para mapear índices
        P = np.full((n, n), None)  # Matriz de predecesores
        C = np.full((n,n), np.inf)
        
        for a,b in G.edges: # por cada par de vertices que definen a un arista
            i, j = nodos.index(a), nodos.index(b)
            C[i, j] = G[a][b]['weight']
            P[i, j] = i  # Predecesor de j es i
        # Establecer la diagonal principal en 0
        
        np.fill_diagonal(C, 0)
        nodos = list(G.nodes)
        # Algoritmo floyd-marshall
        for k in range(n): # nodo intermedio
            for i in range(n): # nodo origen
                for j in range(n): # nodo destino
                    if C[i,k] + C[k,j] < C[i,j]: # pasar por k reduce
                        temp = C[i,j]
                        C[i,j] = C[i,k] + C[k,j] # actualizar el costo actual
                        P[i,j] = P[k,j] # Actualizar predecesor
                        if temp != C[i,j]: # si hubo un cambio
                            print("\nCosto Anterior: ", temp)
                            print(f"{nodos[i]} -> {nodos[j]}: min( {temp}, {nodos[i]}->{nodos[k]}+{nodos[k]}->{nodos[j]} ) ={C[i,j]}")
        return C, P

    def reconstruirCamino(self, C, P, origen, destino):
        G = self.G
        nodos = list(G.nodes)  # Lista de nodos para mapear índices
        i, j = nodos.index(origen), nodos.index(destino)
        if C[i, j] == np.inf:  # No hay camino
            return []

        camino = []
        while j is not None and j != i:
            camino.append((nodos[P[i, j]], nodos[j]))
            j = P[i, j]

        return list(reversed(camino))


    def reconstruirCaminos(self,origen, predecesores: dict):
        aristas = []
        for nodo, predecesor in predecesores.items():
            camino = []
            # nodo: {predecesores}
            anterior = origen
            destino = None
            for a, b in predecesor.items(): # Solo si tiene items
                arista = ( anterior, b)
                anterior = b
                destino = a
                camino.append(arista)

            # anexa el ultimo arista pero, si no tiene items
            if destino is None: # si solo existe un arista
                if self.G.has_edge(anterior, nodo):
                    camino.append((anterior,nodo)) # añadir arista de origen a nodo solo si existe conexión
            else:
                camino.append((anterior,destino))

            aristas.append(camino)

        return aristas

    def dijkstra(self):
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
                paths = self.reconstruirCaminos(origen,predecesores)
                if destino == 'todo':
                    for path in paths:
                        camino+=path
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
        strDistancia = ""
        C, P = self.floydFunc()
        nodos = list(self.G.nodes)
        ci,cj = C.shape
        self.caminos = []
        for i in range(ci):
            for j in range( cj):
                if C[i,j] != np.inf and nodos[i] != nodos[j]:
                    strDistancia += (f"{nodos[i]} -> {nodos[j]}: {C[i, j]}\n")
                    camino = self.reconstruirCamino(C, P, nodos[i], nodos[j])
                    self.caminos.append(camino) # arreglo de camino
        
        self.dibujar_grafo()
        messagebox.showinfo(message=f"Distancias más cortas de todos los nodos:\n{strDistancia}")
    
    def siguienteCamino(self):
        if len(self.caminos) > 0:
            self.camino = self.caminos.pop()
            self.dibujar_grafo()
        else:
            messagebox.showinfo(message="Ya visualizo todos los caminos.")


    def dibujar_grafo(self):
        self.ax.clear()
        nx.draw_networkx_nodes(self.G,self.pos, node_size=200, node_color='#ff5353')
        # etiquetas de nodos
        nx.draw_networkx_labels(self.G, self.pos,font_size=10, font_family="Montserrat", font_color='white', font_weight='bold')
        edges_diff = set(self.G.edges) - set(self.camino)
        edge_labels_diff = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in edges_diff}  # Aristas NO usadas
        edge_labels = {edge: self.G[edge[0]][edge[1]]["weight"] for edge in self.camino if edge in self.G.edges}
        # aristas no usados
        nx.draw_networkx_edges(self.G,self.pos, edgelist=edges_diff,  width=2)
        nx.draw_networkx_edge_labels(self.G,self.pos, edge_labels_diff, font_size=10, font_color='#ff5353',font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec":(1.0, 1.0, 1.0),"fc":(1.0, 1.0, 1.0), "alpha": 0.6}) # por cada arista colocar etiqueta
        # aristas de self.caminos más cortos
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.camino, edge_color='#ff5353', width=2)
        nx.draw_networkx_edge_labels(self.G,self.pos, edge_labels,font_size=10, font_color='#040404',font_family="Montserrat", font_weight='bold', bbox={"boxstyle": "round", "ec":(1.0, 1.0, 1.0),"fc":(1.0, 1.0, 1.0), "alpha": 0.6}) # por cada arista colocar etiqueta

        self.canvas.draw()

    def on_press(self, event):
        if event.xdata is not None and event.ydata is not None:
            for node, (x, y) in self.pos.items():
                if abs(event.xdata - x) < 0.1 and abs(event.ydata - y) < 0.1: # si hizo click en las coordenadas de un nodo
                    self.dragging = node # colocar como objetivo a la key del nodo
                    break

    def on_release(self, event):
        self.dragging = None

    def on_motion(self, event):
        if self.dragging and event.xdata is not None and event.ydata is not None:
            self.pos[self.dragging] = (event.xdata, event.ydata) # actualizar a la nueva posición
            self.dibujar_grafo() #redibujar grafo

# Crear ventana
root = tk.Tk()
app = GrafoInteractivo(root)
root.mainloop()
