import sys
import threading
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from dash import Dash, html
import dash_cytoscape as cyto

# Configuración de entorno para mejor rendimiento gráfico
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-gpu "
    "--use-angle=d3d11 "
    "--enable-webgl "
    "--enable-webgl2 "
    "--enable-webgpu "
    "--enable-accelerated-video-decode "
    "--enable-accelerated-video-encode "
    "--disable-gpu-driver-bug-workarounds"
)
os.environ["QT_OPENGL"] = "hardware"

class DashApp:
    def __init__(self):
        self.app = Dash(__name__)
        self.setup_layout()

    def setup_layout(self):
        elements = [
            {'data': {'id': 'A', 'label': 'Nodo A'}},
            {'data': {'id': 'B', 'label': 'Nodo B'}},
            {'data': {'id': 'C', 'label': 'Nodo C'}},
            {'data': {'source': 'A', 'target': 'B'}},
            {'data': {'source': 'B', 'target': 'C'}}
        ]
        
        self.app.layout = html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                layout={'name': 'cose', 'animate': True},
                style={'width': '100%', 'height': '500px'},
                stylesheet=[
                    {'selector': 'node', 'style': {'label': 'data(label)', 'width': 20, 'height': 20}},
                    {'selector': 'edge', 'style': {'line-color': 'gray'}},
                    {'selector': ':selected', 'style': {'background-color': 'red'}}
                ]
            )
        ])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 + Dash + Cytoscape")
        self.setGeometry(100, 100, 800, 600)
        
        self.browser = QWebEngineView()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.start_dash_server()

    def start_dash_server(self):
        self.dash_app = DashApp()
        
        def run_server():
            # CAMBIO CLAVE: Usar run() en lugar de run_server()
            self.dash_app.app.run(host='127.0.0.1', port=8050, debug=False)
        
        self.thread = threading.Thread(target=run_server)
        self.thread.daemon = True
        self.thread.start()
        
        self.browser.setUrl(QUrl("http://127.0.0.1:8050"))

if __name__ == '__main__':
    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView
    except ImportError:
        print("Error: Necesitas instalar PySide6-WebEngine")
        print("pip install PySide6-WebEngine")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())