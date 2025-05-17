import sys
import json
import os
import tempfile
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication,
QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QInputDialog, QSizePolicy)
from PySide6.QtCore import Slot, Qt, QUrl, QFile, QIODevice, QIODevice, QTextStream
from PySide6.QtGui import QFontDatabase, QColor
import numpy as np
import res_rc
from Arboles import *
from treeVisualizer import *

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = ("--disable-gpu ")

def load_font_from_resource():
    # Cargar fuente desde recursos
    font_file = QFile(":/fonts/redhat.ttf")
    if not font_file.open(QIODevice.ReadOnly):
        print("Error al abrir el archivo de fuente")
        return False
    
    font_data = font_file.readAll()
    font_file.close()
    
    font_id = QFontDatabase.addApplicationFontFromData(font_data)
    return font_id != -1
                        
class MainWindow(QMainWindow):
    def __init__(self, title: str = ' ', w: int = 600, h: int = 300):
        super().__init__()
        load_font_from_resource()
        self.setWindowTitle(title)
        self.setMinimumSize(w, h)
        self.showMaximized()
        
        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("Main")
        self.setCentralWidget(central_widget)
    
        self.main_layout = QHBoxLayout(central_widget)  # Set parent here
        
        self.menu = QWidget()
        self.menu.setLayout(QVBoxLayout())
        self.graph = QWidget()
        self.graph.setLayout(QHBoxLayout())
        
        # Add layouts to main layout with stretch factors
        self.main_layout.addWidget(self.menu, 1)  # Takes 1 part of space
        self.main_layout.addWidget(self.graph, 4)  # Takes 4 parts of space
        
        self.init_menu()
        
        load_font_from_resource()
        # Load stylesheet
        file = QFile(":/styles/main.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print("Failed to load stylesheet:", file.errorString())
    
    def init_menu(self):
        buttons = [
            ("Añadir elemento", "edit", None),
            ("Cargar el árbol desde archivo", "load", None),
            ("Buscar un elemento", "search", None),
            ("Insertar un elemento", "insert", None),
            ("Eliminar un elemento", "delete", None),
            ("Intercambiar un elemento", "exchange", None)
        ]
        
        self.menu.layout().addStretch() # funciona como un resorte, empuja los botones hacia arriba

        for label, btnid, slot in buttons:
            button = QPushButton(label, self.menu)
            button.setObjectName(btnid)
            if slot:
                button.clicked.connect(slot)
            self.menu.layout().addWidget(button)
        
        self.menu.layout().addStretch() # funciona como un resorte, empuja los botones hacia arriba

        # Inicializar grafo
        self.tree = AVLTree()
        self.tree_viz = tree_visualizer_factory(self.graph, self.tree)
        # inicializar grafo
        
        for x in [10,20,30,40,50,11,12,13,14,25,45,56,78]:
            self.tree.insert(x)
        self.tree_viz.draw_tree(self.tree)
    
    def add_node_dialog(self):
        """Diálogo para añadir nuevo nodo"""
        text, ok = QInputDialog.getText(self, 'Añadir nodo', 'Ingrese nombre del nodo:')
        if ok and text:
            # Añadir en posición aleatoria para demostración
            x = np.random.randint(-100, 100)
            y = np.random.randint(-100, 100)
            self.add_node(text, x, y)
        


if __name__ == '__main__':
    
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())