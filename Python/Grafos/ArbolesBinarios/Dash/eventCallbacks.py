from dash import Dash, html, Input, Output, callback, dcc
import dash_cytoscape as cyto
import json

app = Dash()

styles = { # estilo a usar
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 20 * lat, 'y': -20 * long}
    }
    for short, label, long, lat in (
        ('la', 'Los Angeles', 34.03, -118.25),
        ('nyc', 'New York', 40.71, -74),
        ('to', 'Toronto', 43.65, -79.38),
        ('mtl', 'Montreal', 45.50, -73.57),
        ('van', 'Vancouver', 49.28, -123.12),
        ('chi', 'Chicago', 41.88, -87.63),
        ('bos', 'Boston', 42.36, -71.06),
        ('hou', 'Houston', 29.76, -95.37)
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('van', 'la'),
        ('la', 'chi'),
        ('hou', 'chi'),
        ('to', 'mtl'),
        ('mtl', 'bos'),
        ('nyc', 'bos'),
        ('to', 'hou'),
        ('to', 'nyc'),
        ('la', 'nyc'),
        ('nyc', 'bos')
    )
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-2',
        layout={'name': 'preset'},
        elements=edges+nodes,
        style={'width': '100%', 'height': '450px'}
    ),
    # preformatted text
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
    html.P(id='cytoscape-tapNodeData-output'),
    html.P(id='cytoscape-tapEdgeData-output'),
    html.P(id='cytoscape-mouseoverNodeData-output'),
    html.P(id='cytoscape-mouseoverEdgeData-output'),
    # Componente que despliega texto con formato de markdown
    dcc.Markdown(id='cytoscape-selectedNodeData-markdown')
])

# definiendo el callback

@callback(
    # donde colocan los datos?
    # en el elemento pre, se coloca en children, en este caso una cadena
    Output('cytoscape-tapNodeData-json', 'children'),
    # donde se reciben los datos?
    # en nuestro grafo, los datos al tocar un nodo
    Input('cytoscape-event-callbacks-2', 'tapNodeData')
)

def displayTapNodeData(data):
    # serializa un json a una cadena
    # la cadena serializada es retornada y se coloca en children del Pre
    return json.dumps(data, indent=2) # identa con dos espacios

@callback(
    Output('cytoscape-tapNodeData-output', 'children'),
    Input('cytoscape-event-callbacks-2', 'tapNodeData')
)

def displayTapNodeData(data):
    if data: # si no es nulo, desplegar label del nodo
        return "You recently clicked/tapped the city: " + data['label']


@callback(
    Output('cytoscape-tapEdgeData-output', 'children'),
    Input('cytoscape-event-callbacks-2', 'tapEdgeData')
)

def displayTapEdgeData(data):
    if data: # si no es nulo, recuperar los datos de tocar un lado
        # desplegar origen y destino del nodo tocado
        return "You recently clicked/tapped the edge between " + \
               data['source'].upper() + " and " + data['target'].upper()

@callback(
    Output('cytoscape-mouseoverNodeData-output', 'children'),
    Input('cytoscape-event-callbacks-2', 'mouseoverNodeData')
)

def displayTapNodeData(data):
    if data: # si no es nulo, desplegar label del nodo sobre el que pasaste
        return "You recently hovered over the city: " + data['label']


@callback(
    Output('cytoscape-mouseoverEdgeData-output', 'children'),
    Input('cytoscape-event-callbacks-2', 'mouseoverEdgeData')
)

def displayTapEdgeData(data):
    if data: # si no es nulo, desplegar datos del lado sobre el que pasaste
        return "You recently hovered over the edge between " + \
               data['source'].upper() + " and " + data['target'].upper()

# ! RELEVANTE

@callback(
    Output('cytoscape-selectedNodeData-markdown', 'children'),
    Input('cytoscape-event-callbacks-2', 'selectedNodeData')) # datos de seleccion de nodos
def displaySelectedNodeData(data_list):
    if data_list is None: # si es nulos
        return "No city selected."

    cities_list = [data['label'] for data in data_list] # recuperar labels
    # indicar nodos seleccionados
    return "You selected the following cities: " + "\n* ".join(cities_list)





if __name__ == '__main__':
    app.run(debug=True)
