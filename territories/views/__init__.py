from flask import render_template
from territories import territories
from territories.models.graph_nx import NXGraph
from territories.models.voronoi import Voronoi


@territories.route('/')
def index():
    return render_template('index.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = NXGraph('')
    return NXGraph.to_json(graph.nx_g)


@territories.route('/_get_voronoi_data')
def get_voronoi_data():
    graph = NXGraph('d_cluster')
    graph.cal_mds_positions()
    s = graph.cal_cluster_voronoi_positions()
    v = Voronoi(s)
    v.get_constraints_dict()
    return "[" + NXGraph.to_json(graph.nx_g) + "," + s + "]"
