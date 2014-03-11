from flask import render_template
from territories import territories
from territories.models.graph_nx import NXGraph
from territories.models.voronoi import Voronoi
from territories.models.graph_generator import GraphGenerator


@territories.route('/')
def index():
    return render_template('index.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = NXGraph('')
    return NXGraph.to_json(graph.nx_g)


@territories.route('/_get_voronoi_data_d')
def get_voronoi_data_d():
    clustered_graph = NXGraph('d_cluster')
    original_graph = NXGraph('')
    return get_json(original_graph, clustered_graph)


@territories.route('/_get_voronoi_data_r')
def get_voronoi_data_r():
        generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
        g = generator.get_ig()
        cv = generator.community_detection(g)
        original_graph = NXGraph()
        original_graph.nx_g = generator.get_nx()
        clustered_graph = NXGraph()
        clustered_graph.nx_g = generator.convert2nx(cv)
        return get_json(original_graph, clustered_graph)


def get_json(original_graph, clustered_graph):
    clustered_graph.cal_mds_positions()
    s = clustered_graph.cal_cluster_voronoi_positions()
    v = Voronoi(s)
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(c_l_d, c_p_d)
    return "{\"cluster\":" + NXGraph.to_json(clustered_graph.nx_g) + ", \"voronoi\": "+ v.to_json() + ",\"original\":"+ NXGraph.to_json(original_graph.nx_g) +"}"
