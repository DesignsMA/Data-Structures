import sys
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QVBoxLayout, 
                              QHBoxLayout, QMainWindow, QInputDialog)
from PySide6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui

class MainWindow(QMainWindow):
    def __init__(self, title: str = 'Visualizador Simple', w: int = 800, h: int = 600):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(w, h)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("Main")
        self.setCentralWidget(central_widget)
    
        self.main_layout = QHBoxLayout(central_widget)
        
        # Panel de menú
        self.menu = QWidget()
        self.menu.setLayout(QVBoxLayout())
        
        # Área de gráfico
        self.graph_widget = pg.GraphicsLayoutWidget()
        
        # Configurar layout principal
        self.main_layout.addWidget(self.menu, 1)
        self.main_layout.addWidget(self.graph_widget, 4)
        
        # Inicializar elementos
        self.init_menu()
        self.init_graph()
        
        # Diccionario para almacenar nodos por nombre
        self.node_dict = {}
        
    def init_menu(self):
        """Inicializa los botones del menú"""
        self.menu.layout().addStretch()
        
        # Botón para añadir nodo
        add_button = QPushButton("Añadir elemento")
        add_button.clicked.connect(self.add_node_dialog)
        self.menu.layout().addWidget(add_button)
        
        # Espaciador
        self.menu.layout().addStretch()
        
    def init_graph(self):
        """Inicializa el área de visualización"""
        self.plot = self.graph_widget.addPlot()
        self.plot.hideAxis('left')
        self.plot.hideAxis('bottom')
        self.plot.setAspectLocked(True)
        
        # Elementos gráficos
        self.scatter = pg.ScatterPlotItem(size=20, brush=pg.mkBrush(70, 130, 180))
        self.plot.addItem(self.scatter)
        
        # Líneas de conexión
        self.lines = []
        
        # Datos de nodos
        self.node_data = {'pos': [], 'name': []}
        self.node_dict = {}
        
        # Ejemplo inicial
        self.add_demo_nodes()
        
    def add_demo_nodes(self):
        """Añade algunos nodos de demostración"""
        self.add_node("A", 0, 0)
        self.add_node("B", 50, 50)
        self.add_node("C", -50, 50)
        self.add_edge("A", "B")
        self.add_edge("A", "C")
        
    def add_node_dialog(self):
        """Diálogo para añadir nuevo nodo"""
        text, ok = QInputDialog.getText(self, 'Añadir nodo', 'Ingrese nombre del nodo:')
        if ok and text:
            # Añadir en posición aleatoria para demostración
            x = np.random.randint(-100, 100)
            y = np.random.randint(-100, 100)
            self.add_node(text, x, y)
            
    def add_node(self, name, x, y):
        """Añade un nodo al gráfico"""
        # Registrar nodo
        self.node_dict[name] = (x, y)
        self.node_data['pos'].append([x, y])
        self.node_data['name'].append(name)
        
        # Actualizar gráfico
        self.update_graph()
        
    def add_edge(self, node1_name, node2_name):
        """Añade una conexión entre nodos"""
        if node1_name in self.node_dict and node2_name in self.node_dict:
            x1, y1 = self.node_dict[node1_name]
            x2, y2 = self.node_dict[node2_name]
            
            line = pg.PlotCurveItem(
                x=[x1, x2], 
                y=[y1, y2], 
                pen=pg.mkPen('w', width=2))
            
            self.plot.addItem(line)
            self.lines.append(line)
        
    def update_graph(self):
        """Actualiza todos los nodos en el gráfico"""
        if not self.node_data['pos']:
            return
            
        pos = np.array(self.node_data['pos'])
        self.scatter.setData(
            x=pos[:, 0], 
            y=pos[:, 1],
            size=20,
            brush=pg.mkBrush(70, 130, 180),
            data=self.node_data['name'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())