import sys
import json
import os
import tempfile
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication,
QVBoxLayout, QHBoxLayout, QLabel, QMainWindow, QInputDialog, QMenu,
QSplashScreen, QFileDialog, QMessageBox)
from PySide6.QtCore import Slot, Qt, QUrl, QFile, QIODevice, QIODevice, QTextStream
from PySide6.QtGui import QFontDatabase, QPixmap, QAction
import numpy as np
import res_rc
from Arboles import *
from treeVisualizer import *
from popup import *
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = ("--disable-gpu ")
dir_path = os.path.dirname(os.path.realpath(__file__)) # obtener ubicacion actual
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
            ("Cargar el árbol desde archivo", "load", self.load),
            ("Buscar un elemento", "search", None),
            ("Insertar un elemento", "insert", None),
            ("Eliminar un elemento", "delete", None),
            ("Intercambiar un elemento", "exchange", None)
        ]
        
        self.menu.layout().addStretch() # funciona como un resorte, empuja los botones hacia arriba

        for label, btnid, slot in buttons:
            button = QPushButton(label, self.menu)
            button.setObjectName(btnid)
            button.setProperty("class", f"appBtn")
            if slot:
                button.clicked.connect(slot)
            self.menu.layout().addWidget(button)
        self.init_treeSelect()
        self.menu.layout().addStretch() # funciona como un resorte, empuja los botones hacia arriba

        # Inicializar grafo
        self.tree = BinarySearchTree()
        self.tree_viz = TreeVisualizer(self.graph)
        # inicializar grafo
        self.tree_viz.draw_tree(self.tree)
        self.keys = []
        
        
    def init_treeSelect(self):
        self.btnMenu = QPushButton("Tipo de árbol", self.menu)
        self.btnMenu.setObjectName('btnMenu')
        self.btnMenu.setProperty("class", f"appBtn")
        self.btnMenuActions = QMenu(parent=self)
        self.btnMenuActions.setObjectName("btnMenuActions")
        
        self.actions = [
            ("Binario", lambda: self.init_tree(0)),
            ("Binario de busqueda", lambda: self.init_tree(1)),
            ("Balanceado AVL", lambda: self.init_tree(2)),
            ("B | Def. Knuth", lambda: self.init_tree(3)),
        ]
        
        # Agregar acciones dinámicamente
        for name, func in self.actions:
            action = QAction(name, self)
            action.triggered.connect(func)
            self.btnMenuActions.addAction(action)

        # Conectar el botón al menú
        self.btnMenu.setMenu(self.btnMenuActions)
        
        self.menu.layout().addWidget(self.btnMenu)
    def init_tree(self, opt):
        if opt == 0:
            self.tree = BinarySearchTree()
        elif opt == 1:
            self.tree = BinarySearchTree()
        elif opt == 2:
            self.tree = AVLTree()
        elif opt == 3:
            number, ok = QInputDialog.getInt(
                self,                          # Ventana padre
                "Ingrese el orden del árbol.",           # Título
                "Número (3-...):",             # Etiqueta
                value=3,                      # Valor por defecto
                minValue=3,                         # Mínimo
                step=1                         # Incremento/decremento
            )
            if ok:
                self.tree = BTree(m=number)
            else:
                self.tree = BTree(m=3)
                BlurredOverlay(self, "Error. Usando 3 por defecto.").show()
        
        for x in self.keys:
            self.tree.insert(x)
        
        # reiniciar grafo
        self.tree_viz.update_tree_type(self.tree)    
                
    @Slot()
    def load(self, arg):
        errorDiag = BlurredOverlay(self, "Error al abrir archivo.")
        if self.tree is not None: # si se eligio un árbol
            filename = QFileDialog.getOpenFileName(self, "Proporciona el .txt", dir_path,"Archivos de texto (*.txt)")
            try:
                with open(filename[0], 'r') as f:
                    numbers = [int(x) for x in f.read().split(',') if x.strip().isdigit()]
                    if isinstance(self.tree, BTree):
                        self.tree.root = BTreeNode(self.tree.m, is_leaf=True)
                    else:
                        self.tree.root = None
                    self.keys = []
                    for num in numbers:
                        self.tree.insert(num)
                        self.keys.append(num)
                    self.tree_viz.update()
            except Exception as e:
                errorDiag.show()
    
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
    pixmap = QPixmap(":/src/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    
window = MainWindow()
window.show()
# Run the main Qt loop
splash.finish(window)
sys.exit(app.exec())