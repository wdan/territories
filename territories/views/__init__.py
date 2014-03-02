from flask import render_template
from territories import territories
from territories.models.graph import Graph


@territories.route('/')
def index():
    return render_template('index.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = Graph()
    return graph.to_json()
