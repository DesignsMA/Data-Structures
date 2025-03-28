from Grafo import Grafo

# DFS o busqueda profunda
def dfs_profundidad(grafo, inicio):
    verificado = set()  # seguimiento de nodos verificados (aqui se irá viendo el orden del camino)
    pila = [inicio]  # se usa una pila para la busqueda profunda inicializandola con el primer nodo(inicio)
    l=[]

    while pila:  # Continua hasta que la pila esta vacía
        nodo = pila.pop()  # saca el nodo de la pila y lo almacena para ser usado despues
        if nodo not in verificado:
            verificado.add(nodo)  # Verifica el nodo añadiendolo al set para llevar el orden del camino
            l.append(nodo)
            print(nodo)        # Imrpime el nodo actual (para visualizar)
            pila.extend(reversed(grafo.vertices[nodo]))  # Añade nodos hijos a la pila en orden reverso 
    print(l)        

print("Defina los vertices del grafo\n")
vertices = []
while True:
    vertice = input("\nIntroduce un vertice\n-1 para salir : ")
    
    if vertice == "-1":
        print("\nSaliendo...")
        break
    
    if not vertice.isalnum():
        print("El vertice debe ser al menos un caracter o digito.")
        continue
    
    if vertice not in vertices: # si el  vertice  no esta repetido
        vertices.append(vertice)
    else:
        print(f"El vertice '{vertice}' ya existe.")

grafo = Grafo( vertices )
grafo.definirAdjacencia()

inicio = None
print(f"Grafo :\n{grafo}")
while True:
    inicio = input("\nIntroduce el vertice de inicio: ")
    
    if inicio not in vertices:
        print(f"El vertice '{inicio}' no existe en el grafo.")
    else:
        break

# Llamamos a a funcion que creamos dando inicio en el nodo "A"
dfs_profundidad(grafo, inicio)


