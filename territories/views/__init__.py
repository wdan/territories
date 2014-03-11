from flask import render_template
from flask import request
from territories import territories
from territories.models.graph_nx import NXGraph
from territories.models.voronoi import Voronoi
from territories.models.graph_generator import GraphGenerator


width = 0
height = 0
v = None
generator = None


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


@territories.route('/get_aggregate')
def get_aggregate():
    width = request.args.get('width', 1000)
    height = request.args.get('width', 1000)
    shrink = request.args.get('shrink', 50)
    rate = request.args.get('rate', 1)
    generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
    g = generator.get_ig()
    cv = generator.community_detection(g)
    clustered_graph = NXGraph(width, height)
    clustered_graph.nx_g = generator.convert2nx(cv)
    clustered_graph.cal_mds_positions()
    s = clustered_graph.cal_cluster_voronoi_positions()
    v = Voronoi(s, shrink)
    return v.to_json()
    #return get_json(original_graph, clustered_graph)


@territories.route('/get_original')
def get_original():
    original_graph = NXGraph(width, height)
    original_graph.nx_g = generator.get_nx()
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(c_l_d, c_p_d)
    return NXGraph.to_json(original_graph.nx_g)

def get_json(original_graph, clustered_graph):
    clustered_graph.cal_mds_positions()
    s = clustered_graph.cal_cluster_voronoi_positions()
    v = Voronoi(s)
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(c_l_d, c_p_d)
    return "{\"cluster\":" + NXGraph.to_json(clustered_graph.nx_g) + ", \"voronoi\": "+ v.to_json() + ",\"original\":"+ NXGraph.to_json(original_graph.nx_g) +"}"
