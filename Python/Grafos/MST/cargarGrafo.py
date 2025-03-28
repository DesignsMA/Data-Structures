import networkx as nx
import numpy as np

def cargarGrafo(ruta: str):
    try:
        with open(ruta, "r", encoding="UTF-8") as file:
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
                            G.add_edge(nodos[i], nodos[j], weight=peso)
            
            return G
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta}")
    except ValueError as ve:
        print(f"Error en el formato del archivo: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return None
