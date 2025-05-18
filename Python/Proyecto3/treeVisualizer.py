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
    
    def _binary_layout(self, G, min_spacing=80, baseline_x=200, baseline_y=100):
        """Layout especializado para árboles binarios con separación mínima entre subárboles del nodo raíz"""
        pos = {}
        if not G.nodes:
            return pos

        root = [n for n in G.nodes if G.in_degree(n) == 0][0]
        successors = list(G.successors(root))

        left_pos = {}
        right_pos = {}

        # Layout para subárbol izquierdo
        if len(successors) >= 1:
            self._calculate_binary_positions(
                G, successors[0], left_pos,
                x=0, y=1,
                spacing=240,
                min_spacing=min_spacing,
                baseline_y=baseline_y
            )

        # Layout para subárbol derecho
        if len(successors) == 2:
            self._calculate_binary_positions(
                G, successors[1], right_pos,
                x=0, y=1,
                spacing=240,
                min_spacing=min_spacing,
                baseline_y=baseline_y
            )

        # Calcular ancho del subárbol izquierdo y derecho
        min_left_x = min((x for x, _ in left_pos.values()), default=0)
        max_left_x = max((x for x, _ in left_pos.values()), default=0)
        min_right_x = min((x for x, _ in right_pos.values()), default=0)
        max_right_x = max((x for x, _ in right_pos.values()), default=0)

        # Ajustar para evitar colisiones entre subárboles
        left_shift = - (max_left_x + baseline_x / 2)
        right_shift = -min_right_x + (max_left_x + baseline_x / 2)

        for n in left_pos:
            x, y = left_pos[n]
            pos[n] = (x + left_shift, y)

        for n in right_pos:
            x, y = right_pos[n]
            pos[n] = (x + right_shift, y)

        # Asignar posición del nodo raíz en el centro
        pos[root] = (0, 0)

        return pos

    def _calculate_binary_positions(self, G, node, pos, x, y, spacing, min_spacing, baseline_y):
        """Calcula posiciones recursivas con espaciado adaptativo"""
        if node not in G.nodes:
            return

        # Obtener hijos
        successors = list(G.successors(node))

        # Detectar degeneración
        is_right_heavy = len(successors) > 0 and all(
            G.nodes[succ]['label'] > G.nodes[node]['label'] for succ in successors
        )
        is_left_heavy = len(successors) > 0 and all(
            G.nodes[succ]['label'] < G.nodes[node]['label'] for succ in successors
        )

        # Ajustar espaciado
        spacing = max(spacing * 0.7, min_spacing)

        # Posiciones de hijos
        child_positions = {}
        if len(successors) >= 1:
            self._calculate_binary_positions(
                G, successors[0], child_positions,
                x - spacing if not is_right_heavy else x + spacing * 0.5,
                y + 1,
                spacing,
                min_spacing,
                baseline_y
            )

        if len(successors) >= 2:
            self._calculate_binary_positions(
                G, successors[1], child_positions,
                x + spacing if not is_left_heavy else x - spacing * 0.5,
                y + 1,
                spacing,
                min_spacing,
                baseline_y
            )

        # Si hay dos hijos, centrar el padre
        if len(successors) == 2:
            x1 = child_positions[successors[0]][0]
            x2 = child_positions[successors[1]][0]
            x = (x1 + x2) / 2

        # Guardar posición actual
        pos[node] = (x, y * baseline_y)
        pos.update(child_positions)

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
                    "nodeDistance": 200
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