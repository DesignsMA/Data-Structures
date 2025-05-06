import sys
import threading
import os
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow)
from PySide6.QtCore import Slot, Qt, QUrl, QTextStream, QFile, QIODevice
from PySide6.QtGui import QFontDatabase, QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import res_rc
from dash import Dash, html, Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dcc

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
        
        self.initMenu()
        
        load_font_from_resource()
        # Load stylesheet
        file = QFile(":/styles/main.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print("Failed to load stylesheet:", file.errorString())
    
    def initMenu(self):
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
        self.view = QWebEngineView() # visualizador web
        self.view.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
        self.view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.ForceDarkMode, True) 
        self.view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True) 
        self.view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True) 
        self.start_dash_server()
        self.graph.layout().addWidget(self.view)

    def start_dash_server(self):
        self.dash_app = DashApp() # instanciar grafo
        
        def run_server():
            self.dash_app.app.run(host='127.0.0.1', port=8050, debug=False)
        
        self.thread = threading.Thread(target=run_server)
        self.thread.daemon = True
        self.thread.start()
        
        self.view.setUrl(QUrl("http://127.0.0.1:8050"))
        self.view.update()

class DashApp:
    def __init__(self):
        self.app = Dash(__name__, prevent_initial_callbacks=True)
        self.setup_layout()

    def setup_layout(self):
        elements = [
            {'data': {'id': 'A', 'label': 'Nodo A'}},
            {'data': {'id': 'B', 'label': 'Nodo B'}},
            {'data': {'id': 'C', 'label': 'Nodo C'}},
            {'data': {'source': 'A', 'target': 'B'}},
            {'data': {'source': 'B', 'target': 'C'}}
        ]
        
        default_stylesheet = [
                    {
                        'selector': 'node', 
                        'style': {'label': 'data(label)',
                        'width': 20, 'height': 20}
                    },
                    {
                        'selector': 'edge',
                        'style': {'line-color': 'gray'}
                    },
                    {'selector': ':selected',
                     'style': {'background-color': 'red'}
                    }
                ]
        
        self.app.layout = html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                layout={'name': 'preset', 'animate': True},
                style={'width': '100vw-200px', 'height': '95vh'},
                stylesheet=default_stylesheet
            ),
            dcc.Row(
                id='controlPanel',
                align='center',
                class_name='editor',
                label="Editar Grafo",
                children=
                [
                    html.Button("Insertar nodo", id='btn1'),
                    html.Button("Eliminar nodo", id='btn2'),
                    html.Button("Intercambiar nodos", id='btn3'),
                    html.Div(id='log')
                ]
            )
        ])

        self.app.clientside_callback(
            """
            function(){
                console.log(dash_clientside.callback_context);
                const triggered_id = dash_clientside.callback_context.triggered_id;
                return "triggered id: " + triggered_id
            }
            """,
            Output("log", "children"),
            Input("btn1", "n_clicks"),
            Input("btn2", "n_clicks"),
            Input("btn3", "n_clicks"),
        )


if __name__ == '__main__':
    
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())