from abc import ABC, abstractmethod
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import networkx as nx
from pyvis.network import Network

class TreeVisualizerBase(ABC):
    def __init__(self, parent_widget):
        self.tree = None
        self.web_view = QWebEngineView(parent_widget)
        
        # Configuración común del viewport
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        
        parent_widget.layout().setContentsMargins(0, 0, 0, 0)
        parent_widget.layout().setSpacing(0)
        parent_widget.layout().addWidget(self.web_view)
    
    @abstractmethod
    def _build_networkx_graph(self, G, node, parent_id=None):
        """Método abstracto para construir el grafo NetworkX"""
        pass
    
    def draw_tree(self, tree):
        """Dibuja el árbol usando NetworkX y PyVis"""
        self.tree = tree
        if not self.tree or not self.tree.root:
            return
            
        G = nx.DiGraph()
        self._build_networkx_graph(G, self.tree.root)
        pos = self._hierarchical_layout(G)
        html = self._generate_pyvis_html(G, pos)
        self.web_view.setHtml(html)
    
    def _hierarchical_layout(self, G):
        """Calcula posiciones jerárquicas (común para todos los árboles)"""
        levels = {}
        root = [n for n in G.nodes if G.in_degree(n) == 0][0]
        
        # Asignar niveles
        queue = [(root, 0)]
        while queue:
            node, level = queue.pop(0)
            levels[node] = level
            for successor in G.successors(node):
                queue.append((successor, level + 1))
        
        # Calcular posiciones
        pos = {}
        max_level = max(levels.values()) if levels else 0
        
        for level in range(max_level + 1):
            nodes_in_level = [n for n in levels if levels[n] == level]
            level_width = len(nodes_in_level)
            
            for i, node in enumerate(nodes_in_level):
                x = (i + 0.5) * (800 / (level_width + 1))
                y = level * 150 + 50
                pos[node] = (x, y)
        
        return pos
    
    def _generate_pyvis_html(self, G, pos, node_color='#FF2323', edge_color='#FF2D2D49', shape='circle'):
        """Genera HTML con PyVis (configurable por subclases)"""
        nt = Network("100vh", "100vw-40px", bgcolor='#161616', notebook=False, cdn_resources='remote')
        
        # Añadir nodos
        for node in G.nodes:
            x, y = pos[node]
            nt.add_node(
                node,
                label=G.nodes[node]['label'],
                x=x,
                y=y,
                shape=shape,
                color=node_color,
                borderWidth=0,
                font={'size': 12, 'color':'#ffffff'},
                margin=10
            )
        
        # Añadir aristas
        for edge in G.edges:
            nt.add_edge(edge[0], edge[1], width=2, color=edge_color)
        
        # Configuración común
        nt.set_options("""
        {
            "physics": {
                "enabled": false,
                "hierarchicalRepulsion": {
                    "centralGravity": 0,
                    "nodeDistance": 120
                }
            }
        }
        """)
        
        return nt.generate_html()
    
    def clear(self):
        self.web_view.setHtml("")
    
    def update(self):
        if self.tree:
            self.draw_tree(self.tree)
            
class BinaryTreeVisualizer(TreeVisualizerBase):
    def _build_networkx_graph(self, G, node, parent_id=None):
        """Construye el grafo para un árbol binario"""
        if node is None:
            return
            
        node_id = id(node)
        label = str(node.value)
        G.add_node(node_id, label=label)
        
        if parent_id is not None:
            G.add_edge(parent_id, node_id)
        
        # Recursivamente agregar hijos izquierdo y derecho
        self._build_networkx_graph(G, node.left, node_id)
        self._build_networkx_graph(G, node.right, node_id)
    
    def _hierarchical_layout(self, G):
        """Layout especializado para árboles binarios con espaciado adecuado"""
        pos = {}
        if not G.nodes:
            return pos
            
        root = [n for n in G.nodes if G.in_degree(n) == 0][0]
        self._calculate_binary_positions(G, root, pos, x=0, y=0, spacing=120, depth=1)
        return pos
    
    def _calculate_binary_positions(self, G, node, pos, x, y, spacing, depth):
        """Calcula posiciones recursivas con espaciado adaptativo"""
        if node not in G.nodes:
            return
            
        pos[node] = (x*2, y * 100)  # Multiplicamos y por 100 para mejor espaciado vertical
        
        # Reducir el espaciado con la profundidad pero mantener mínimo
        new_spacing = max(spacing * 0.6, 0.8)  # No permitir que sea menor a 0.8
        new_depth = depth + 1
        
        # Calcular posiciones de hijos
        successors = list(G.successors(node))
        if len(successors) >= 1:  # Hijo izquierdo
            self._calculate_binary_positions(
                G, successors[0], pos, 
                x - spacing, y + 1, 
                new_spacing, new_depth
            )
        if len(successors) >= 2:  # Hijo derecho
            self._calculate_binary_positions(
                G, successors[1], pos, 
                x + spacing, y + 1, 
                new_spacing, new_depth
            )
    
    def _generate_pyvis_html(self, G, pos):
        """Personalización para árboles binarios"""
        return super()._generate_pyvis_html(
            G, pos, 
            node_color="#F32121",  # Azul para nodos
            edge_color="#FF1D043E"   # Azul claro para aristas
        )

class BTreeVisualizer(TreeVisualizerBase):
    def _build_networkx_graph(self, G, node, parent_id=None):
        """Construye el grafo para un B-tree"""
        node_id = id(node)
        label = " | ".join(map(str, node.keys))
        G.add_node(node_id, label=label)
        
        if parent_id is not None:
            G.add_edge(parent_id, node_id)
        
        if not node.is_leaf:
            for child in node.children:
                self._build_networkx_graph(G, child, node_id)
    
    def _generate_pyvis_html(self, G, pos):
        """Personalización para B-trees"""
        return super()._generate_pyvis_html(
            G, pos,
            node_color="#F32121",  # Azul para nodos
            edge_color="#FF1D043E",   # Azul claro para aristas
            shape='box'
        )

def tree_visualizer_factory(parent_widget, tree):
    """Factory polimórfico para visualizadores de árboles"""
    # Detección de tipo para B-tree
    if hasattr(tree, 'root') and hasattr(tree.root, 'is_leaf'):
        return BTreeVisualizer(parent_widget)
    # Detección de tipo para árbol binario
    elif tree.root is None:
        return BinaryTreeVisualizer(parent_widget)

    else:
        raise ValueError(f"Tipo de árbol no soportado: {type(tree)}")