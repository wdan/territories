from flask import render_template
from territories import territories
from territories.models.graph_nx import NXGraph


@territories.route('/')
def index():
    return render_template('index.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = NXGraph()
    return NXGraph.to_json(graph.nx_g)
