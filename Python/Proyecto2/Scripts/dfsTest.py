import networkx as nx
import matplotlib.pyplot as plt # usado para graficar los nodos
def generar_posiciones_arbol(G: nx.Graph, root):
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

def dfs_profundidad(grafo, inicio):
    verificado = set()  # Seguimiento de nodos visitados
    pila = [inicio]  # Se usa una pila para la búsqueda en profundidad
    recorrido_aristas = []  # Lista para almacenar las aristas recorridas

    while pila:  # Mientras la pila no esté vacía
        nodo = pila.pop()  # Extrae el nodo de la pila
        if nodo not in verificado:
            verificado.add(nodo)  # Marca el nodo como visitado
            for vecino in reversed(list(grafo.neighbors(nodo))):  # Recorre los vecinos en orden inverso
                if vecino not in verificado:
                    recorrido_aristas.append((nodo, vecino))  # Agrega la arista al recorrido
                    pila.append(vecino)  # Agrega el vecino a la pila

    return recorrido_aristas  # Retorna la lista de aristas recorridas

G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)])
nx.draw(G, with_labels=True, font_weight='bold')

resultado = dfs_profundidad(G, 1)
H = nx.Graph()
H.add_edges_from(resultado)
subax2 = plt.subplot(122) #subplot, (ncols, nrows, index)
nx.draw(H, with_labels=True, font_weight='bold')
plt.show()
print(resultado)  # Imprime las aristas en orden de recorrido