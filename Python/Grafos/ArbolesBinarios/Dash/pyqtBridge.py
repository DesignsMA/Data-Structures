import sys
import random
import json
import threading
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                              QVBoxLayout, QWidget, QPushButton)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from dash import Dash, html, dcc, Input, Output, no_update
import dash_cytoscape as cyto
import os
# Estado inicial del grafo
initial_elements = [
    {'data': {'id': 'A', 'label': 'Nodo A'}},
    {'data': {'id': 'B', 'label': 'Nodo B'}},
    {'data': {'source': 'A', 'target': 'B'}}
]

# Variable global para sincronización
last_update = {"timestamp": 0}

def create_dash_app():
    app = Dash(__name__)
    
    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape',
            elements=initial_elements,
            layout={'name': 'cose'},
            style={'width': '100%', 'height': '500px'},
            stylesheet=[
                {'selector': 'node', 'style': {'label': 'data(label)'}},
                {'selector': 'edge', 'style': {'curve-style': 'bezier'}}
            ]
        ),
        dcc.Store(id='graph-store', data={
            'elements': initial_elements,
            'last_update': 0
        }),
        dcc.Interval(  # Incrementa n_intervals en el intervalo de 0.5 s
            id='interval-component',
            interval=500,  # Medio segundo
            n_intervals=0
        ),
        html.Div(id='dummy-output', style={'display': 'none'})
    ])
    
    # Callback para actualizar el store
    @app.callback(
        Output('graph-store', 'data'),
        Input('interval-component', 'n_intervals'),
        prevent_initial_call=True
    )
    def check_for_updates(_):
        global last_update
        current_ts = last_update["timestamp"]
        if current_ts > app.last_update_ts:
            app.last_update_ts = current_ts
            return {
                'elements': app.current_elements,
                'last_update': current_ts
            }
        return no_update
    
    # Callback para actualizar el grafo
    @app.callback(
        Output('cytoscape', 'elements'),
        Input('graph-store', 'data')
    )
    def update_graph(data):
        return data['elements']
    
    # Inicializar variables en la app
    app.last_update_ts = 0
    app.current_elements = initial_elements
    
    return app

class GraphController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_dash_integration()
        
    def setup_ui(self):
        self.setWindowTitle("Controlador de Grafo Avanzado")
        self.setGeometry(100, 100, 1000, 700)
        
        layout = QVBoxLayout()
        
        # Visor del grafo
        self.browser = QWebEngineView()
        layout.addWidget(self.browser, stretch=5)
        
        # Panel de control
        control_widget = QWidget()
        control_layout = QVBoxLayout()
        
        self.btn_add_node = QPushButton("Añadir Nodo Aleatorio")
        self.btn_add_node.clicked.connect(self.add_random_node)
        
        self.btn_add_edge = QPushButton("Añadir Arista Aleatoria")
        self.btn_add_edge.clicked.connect(self.add_random_edge)
        
        self.btn_reset = QPushButton("Reiniciar Grafo")
        self.btn_reset.clicked.connect(self.reset_graph)
        
        control_layout.addWidget(self.btn_add_node)
        control_layout.addWidget(self.btn_add_edge)
        control_layout.addWidget(self.btn_reset)
        control_widget.setLayout(control_layout)
        
        layout.addWidget(control_widget, stretch=1)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def setup_dash_integration(self):
        self.dash_app = create_dash_app()
        self.dash_thread = threading.Thread(
            target=lambda: self.dash_app.run(host='127.0.0.1', port=8050, debug=False),
            daemon=True
        )
        self.dash_thread.start()
        self.browser.setUrl(QUrl("http://127.0.0.1:8050"))
    
    def update_dash(self, new_elements):
        global last_update
        self.dash_app.current_elements = new_elements
        last_update["timestamp"] += 1
        
        js_code = f"""
        if (typeof DashClientside !== 'undefined') {{
            DashClientside.setProps('graph-store', {{
                data: {{
                    elements: {json.dumps(new_elements)},
                    last_update: {last_update["timestamp"]}
                }}
            }});
        }} else {{
            setTimeout(function() {{
                {js_code}
            }}, 100);
        }}
        """
        self.browser.page().runJavaScript(js_code)
    
    def add_random_node(self):
        elements = self.dash_app.current_elements
        node_id = f"N{random.randint(100, 999)}"
        new_node = {'data': {'id': node_id, 'label': node_id}}
        elements.append(new_node)
        self.update_dash(elements)
    
    def add_random_edge(self):
        elements = self.dash_app.current_elements
        nodes = [e['data']['id'] for e in elements if 'source' not in e['data']]
        if len(nodes) >= 2:
            source, target = random.sample(nodes, 2)
            elements.append({'data': {'source': source, 'target': target}})
            self.update_dash(elements)
    
    def reset_graph(self):
        self.dash_app.current_elements = initial_elements.copy()
        self.update_dash(self.dash_app.current_elements)
        
if __name__ == '__main__':
    # Configuración de entorno para mejor rendimiento
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --enable-webgl"
    os.environ["QT_OPENGL"] = "angle"
    
    # Iniciar aplicación
    qt_app = QApplication(sys.argv)
    controller = GraphController()
    controller.show()
    sys.exit(qt_app.exec())