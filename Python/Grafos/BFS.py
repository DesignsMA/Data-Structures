#Recorrido por amplitud
from Estructuras import Cola
from Grafo import Grafo

def bfs_amplitud(grafo: Grafo, inicio):
    espera = set()  # conjunto de vertices o nodos en espera
    cola = Cola()  # instancia de clase Cola
    cola.encolar(inicio) # encolar  (marcar como listo) al vertice inicial
    recorridoAmplitud = { grafo.listaVertices[i]: [] for i in range(grafo.n) } # diccionario de grafo resultante
    
    espera.update(recorridoAmplitud.keys()) # colocar vertices en espera
    espera.difference_update(inicio) # eliminar de la lista de espera | marcar listo
    
    while not cola.esta_vacia():  # Continua hasta que la cola esta vacía
        nodo = cola.desencolar()  # saca el nodo de la cola y lo almacena para ser usado despues
        print(nodo) # Imprime el nodo actual (para visualizar)
        for vertice in grafo.vertices[nodo]: #recorrer lista de vertices adyacentes al nodo
            if vertice in espera: # si el vertice actual esta en espera
                cola.encolar(vertice) # encolar vertice
                recorridoAmplitud[nodo].append(vertice) # añadir adyacentes en la lista del nodo
                espera.difference_update(vertice) # eliminar de la lista de espera | marcar listo
                
    return recorridoAmplitud

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
    
res = Grafo( diccionarioAdjacencia=bfs_amplitud(grafo, inicio) )


print("Representación | Grafo del arbol resultante :\n")
print(res)


