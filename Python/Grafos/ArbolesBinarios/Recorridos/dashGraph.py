from dash import Dash, html, dcc, Input, Output, no_update
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

class DashApp:
    def __init__(self):
        self.app = Dash(__name__)
        self.setup_layout()

    def setup_layout(self):
        elements = [
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
        
        self.app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    # Columna para el grafo
                    dbc.Col(
                        cyto.Cytoscape(
                            id='cytoscape',
                            elements=elements,
                            layout={'name': 'circle'},
                            style={'width': '100%', 'height': '500px'},
                            stylesheet=[
                                {'selector': 'node', 'style': {'label': 'data(label)'}},
                                {'selector': 'edge', 'style': {'curve-style': 'bezier'}}
                            ]
                        ),
                        width=8
                    ),
                    
                    # Columna para los controles
                    dbc.Col(
                        [
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Button("Añadir Nodo", id="btn-add-node", color="primary", className="mb-2"),
                                                    dbc.Button("Eliminar Nodo", id="btn-delete-node", color="danger", className="mb-2"),
                                                    dbc.Button("Intercambiar Nodos", id="btn-swap-nodes", color="warning", className="mb-2"),
                                                ],
                                                className="d-grid gap-2"
                                            )
                                        ],
                                        label="Editar Grafo"
                                    ),
                                    dbc.Tab(
                                        "Otras herramientas pueden ir aquí",
                                        label="Opciones"
                                    )
                                ]
                            ),
                            html.Div(id='output-message', className="mt-3")
                        ],
                        width=4
                    )
                ]
            )
        ],
        fluid=True,
        className="p-4"
    )
    
    # Callbacks para los botones
    @app.callback(
        Output('output-message', 'children'),
        [
            Input('btn-add-node', 'n_clicks'),
            Input('btn-delete-node', 'n_clicks'),
            Input('btn-swap-nodes', 'n_clicks')
        ],
        prevent_initial_call=True
    )
    def handle_button_clicks(add_clicks, delete_clicks, swap_clicks):
        ctx = dash.callback_context
        
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Solo imprimimos el ID del botón (en una aplicación real aquí iría la lógica)
        print(f"Botón presionado: {button_id}")
        
        return f"Acción solicitada: {button_id.replace('btn-', '').replace('-', ' ')}"
