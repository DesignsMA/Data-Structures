from dash import Dash, html # manejo de pagina | callbacks
import dash_cytoscape as cyto # manejo de grafos con componentes de dash

app = Dash()

app.layout = html.Div([ # wrapper del componente div de html
    cyto.Cytoscape( # Libreria de componentes de visualizacion de grafos
        id='cytoscape-basic',
        layout={ 'name': 'preset'}, # layout del grafo, definida por nosotros
        style={'width': '100%', 'height': '100%'},
        elements=[ # definiendo elementos
            # nodos
            {
                'data': {'id': 'one', 'label': 'node1'}, # id, label
                'position': {'x': 50, 'y': 50} # posiciones en preset
            },
            {
                'data': {'id': 'two', 'label': 'node2'}, # id, label
                'position': {'x': 50, 'y': 100} # posiciones en preset
            },
            
            # edges
            
            {
                'data': {'source': 'one', 'target': 'two', 'label': 'N1 to N2'}
                
            }
        ]
    ) 
])

if __name__ == '__main__': # ejecutar con depuración
    app.run(debug=True)