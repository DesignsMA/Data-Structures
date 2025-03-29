# 🌳 Guardianes del Bosque - Algoritmos para la Conservación

**Objetivo**:  
Programa de capacitación que aplica algoritmos de grafos para la conservación de bosques. Los participantes aprenden a optimizar rutas de limpieza y reciclaje, recibiendo un certificado como *"Guardián del Bosque"*.

---

## 🔍 Funcionalidades por Implementar

### 1. **Exploración de Ecosistemas**  
**Propósito**: Identificar zonas contaminadas aleatorias y planificar rutas de recolección.  

| **BFS**   | Encontrar la zona contaminada **más cercana** (menor número de saltos). |
| **DFS**   | Exploración profunda para detectar contaminación en zonas ocultas.      |

### 2. **Optimización de Rutas de Recolección**  
**Propósito**: Calcular rutas óptimas para transporte de residuos (minimizar distancia/costo).  

| **Dijkstra**      | Ruta más corta desde un punto inicial (ej: base → zona contaminada).                        |
| **Floyd-Warshall**| Rutas más cortas entre **todas** las zonas (útil para múltiples centros de reciclaje).      |


### 3.Diseño de Redes Ecológicas (Prim y Kruskal)
Propósito:
Construir un sistema eficiente de estaciones de reciclaje con la menor cantidad de recursos. Las estaciones
de reciclaje serán ubicadas dentro de las zonas identificadas.
Métodos:
Prim: Es útil si las conexiones entre zonas son numerosas, es decir se tiene un bosque denso. Si el número
de zonas E es cercano al número máximo posible de caminos (V(V−1) /2, el bosque es denso.
Kruskal: Se usa si las zonas están muy dispersas y hay pocos caminos. Si el número de caminos E es
cercano a la cantidad mínima () necesaria para conectar todas las zonas (V−1), el bosque es disperso.
Temas para utilizar

---

### 🛠️ Requisitos Técnicos  
- Grafo no dirigido con pesos (distancias en km).  
- Zonas contaminadas marcadas aleatoriamente.  
- Visualización interactiva del bosque y rutas.  

---

### 🌟 Certificación  
Al completar las actividades, los usuarios reciben un certificado digital como *"Guardián del Bosque"*.  
