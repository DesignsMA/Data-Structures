from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
import networkx as nx
from pyvis.network import Network

class TreeVisualizer:
    def __init__(self, parent_widget):
        self.tree = None
        self.tree_type = None  # 'binary' o 'b-tree'
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
    
    def set_tree_type(self, tree):
        """Determina el tipo de árbol basado en sus características"""
        if hasattr(tree, 'root') and hasattr(tree.root, 'is_leaf'):
            self.tree_type = 'b-tree'
        else:
            self.tree_type = 'binary'
    
    def update_tree_type(self, new_tree):
        """Actualiza el tipo de árbol y recalcula la visualización"""
        self.set_tree_type(new_tree)
        self.tree = new_tree
        self.update()
    
    def _build_networkx_graph(self, G, node, parent_id=None):
        """Construye el grafo NetworkX según el tipo de árbol"""
        if node is None:
            return
            
        node_id = id(node)
        
        if self.tree_type == 'binary':
            label = str(node.value)
            G.add_node(node_id, label=label)
            
            if parent_id is not None:
                G.add_edge(parent_id, node_id)
            
            # Recursivamente agregar hijos izquierdo y derecho
            self._build_networkx_graph(G, node.left, node_id)
            self._build_networkx_graph(G, node.right, node_id)
            
        elif self.tree_type == 'b-tree':
            label = " | ".join(map(str, node.keys))
            G.add_node(node_id, label=label)
            
            if parent_id is not None:
                G.add_edge(parent_id, node_id)
            
            if not node.is_leaf:
                for child in node.children:
                    self._build_networkx_graph(G, child, node_id)
    
    def draw_tree(self, tree):
        """Dibuja el árbol usando NetworkX y PyVis"""
        self.tree = tree
        self.set_tree_type(tree)
        
        if not self.tree or (hasattr(self.tree, 'root') and not self.tree.root):
            return
            
        G = nx.DiGraph()
        self._build_networkx_graph(G, self.tree.root)
        
        # Asegurarnos de que hay nodos antes de calcular posiciones
        if len(G.nodes) == 0:
            return
        
        pos = self._calculate_layout(G)
        html = self._generate_pyvis_html(G, pos)
        self.web_view.setHtml(html)
    
    def _calculate_layout(self, G):
        """Calcula posiciones según el tipo de árbol"""
        if self.tree_type == 'binary':
            return self._binary_layout(G)
        else:
            return self._hierarchical_layout(G)
    
    def _hierarchical_layout(self, G):
        """Layout jerárquico genérico para B-trees"""
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
    
    def _binary_layout(self, G):
        """Layout especializado para árboles binarios"""
        pos = {}
        if not G.nodes:
            return pos
            
        root = [n for n in G.nodes if G.in_degree(n) == 0][0]
        self._calculate_binary_positions(G, root, pos, x=0, y=0, spacing=120, depth=1)
        return pos
    
    def _calculate_binary_positions(self, G, node, pos, x, y, spacing, depth):
        """Calcula posiciones recursivas con espaciado adaptativo mejorado"""
        if node not in G.nodes:
            return
        
        # Asignar posición actual
        pos[node] = (x, y * 100)
        
        # Obtener sucesores (hijos)
        successors = list(G.successors(node))
        
        # Detectar si el árbol es degenerado (todos los nodos a un lado)
        is_right_heavy = len(successors) > 0 and all(
            G.nodes[succ]['label'] > G.nodes[node]['label'] for succ in successors
        )
        is_left_heavy = len(successors) > 0 and all(
            G.nodes[succ]['label'] < G.nodes[node]['label'] for succ in successors
        )
        
        # Ajustar espaciado para árboles degenerados
        if is_right_heavy or is_left_heavy:
            spacing = max(spacing * 0.8, 60)  # Reducir menos el espaciado para degenerados
        else:
            spacing = max(spacing * 0.6, 40)  # Espaciado normal para árboles balanceados
        
        # Calcular posiciones de hijos
        if len(successors) >= 1:  # Hijo izquierdo
            child_x = x - spacing if not is_right_heavy else x + spacing * 0.3
            self._calculate_binary_positions(
                G, successors[0], pos, 
                child_x, y + 1, 
                spacing, depth + 1
            )
        
        if len(successors) >= 2:  # Hijo derecho
            child_x = x + spacing if not is_left_heavy else x - spacing * 0.3
            self._calculate_binary_positions(
                G, successors[1], pos, 
                child_x, y + 1, 
                spacing, depth + 1
            )            
    def _generate_pyvis_html(self, G, pos):
        """Genera HTML con PyVis según el tipo de árbol"""
        if self.tree_type == 'binary':
            node_color = '#F32121'
            edge_color = '#FF1D043E'
            shape = 'circle'
        else:  # b-tree
            node_color = '#F32121'
            edge_color = '#FF1D043E'
            shape = 'box'
        
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