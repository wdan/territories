from flask import render_template
from flask import request
from territories import territories
from territories.models.graph_nx import NXGraph
from territories.models.voronoi import Voronoi
from territories.models.graph_generator import GraphGenerator
from territories.models.graph_importer import GraphImporter

width = 0
height = 0
v = None
generator = None
g = None
rate = 1


@territories.route('/')
def index():
    return render_template('territories.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = NXGraph('')
    return NXGraph.to_json(graph.nx_g)


@territories.route('/_get_voronoi_data_d')
def get_voronoi_data_d():
    clustered_graph = NXGraph('d_cluster')
    original_graph = NXGraph('')
    return get_json(original_graph, clustered_graph)


@territories.route('/get_polygon')
def get_aggregate():
    global g, v, rate, generator
    width = int(request.args.get('width', 1000))
    height = int(request.args.get('height', 1000))
    shrink = int(request.args.get('shrink', 50))
    rate = float(request.args.get('rate', 1))
    #generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
    #g = generator.get_ig()
    g = GraphImporter("").get_hugo()
    cv = GraphGenerator.community_detection(g)
    clustered_graph = NXGraph('r_cluster', width, height)
    clustered_graph.nx_g = GraphGenerator.convert2nx(cv)
    s = clustered_graph.cal_cluster_voronoi_positions()
    v = Voronoi(s, shrink)
    return v.to_json()


@territories.route('/get_original')
def get_original():
    original_graph = NXGraph(width, height)
    original_graph.nx_g = GraphGenerator.convert2nx(g)
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(rate, c_l_d, c_p_d)
    return NXGraph.to_json(original_graph.nx_g)
