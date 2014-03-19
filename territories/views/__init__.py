# -*- coding: utf-8 -*-

import networkx as nx
import json

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
g = None
orig = None
name = ""
rate = 1
clustered_graph = None
detection = False


@territories.route('/')
def index():
    return render_template('territories.html')


@territories.route('/_get_graph_data')
def get_data():
    graph = NXGraph('')
    return NXGraph.to_json(graph.nx_g)


@territories.route('/select_voronoi')
def select_voronoi():
    global v
    src = int(request.args.get('src', -1))
    tgt = int(request.args.get('tgt', -1))
    s = clustered_graph.cal_cluster_voronoi_positions(src, tgt)
    v = Voronoi(s)
    return v.to_json()


@territories.route('/get_polygon')
def get_aggregate():
    global detection, orig, g, v, name, rate, generator, clustered_graph
    name = request.args.get('name', 'random')
    width = int(request.args.get('width', 1000))
    height = int(request.args.get('height', 1000))
    rate = float(request.args.get('rate', 1))
    detection = False
    if name == "random":
        generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
        orig = generator.get_ig()
        detection = True
    elif name == "hugo":
        orig = GraphImporter("").get_hugo()
        del orig.vs["id"]
        detection = True
    elif name == "book":
        orig = GraphImporter("").get_books()
        del orig.vs["id"]
        detection = True
    elif name == "football":
        orig = GraphImporter("").get_football()
        del orig.vs["id"]
    elif name == "school":
        orig = GraphImporter("").get_school()
        del orig.vs["id"]
    elif name == "dblp-os":
        orig = GraphImporter("").get_dblp_os()
        #orig = GraphImporter("").get_dblp_sub(orig, rate)
    elif name == "dblp-os-paper":
        orig = GraphImporter("").get_dblp_os_paper()
    elif name == "dblp-vis-paper":
        orig = GraphImporter("").get_dblp_vis_paper()
    elif name == 'dblp-vis-big':
        orig = GraphImporter("").get_dblp_vis_big()
    g = orig.copy()
    if detection:
        cv = GraphGenerator.community_detection(GraphImporter.remove_attributes(g))
        clustered_graph = NXGraph('r_cluster', width, height)
        clustered_graph.nx_g = GraphGenerator.convert2nx(cv)
    else:
        g = GraphGenerator.convert2nx(g)
        clustered_graph = NXGraph('r_cluster', width, height)
        clustered_graph.nx_g = NXGraph.mark_community(g)
    s = clustered_graph.cal_cluster_voronoi_positions()
    v = Voronoi(s)
    return v.to_json()


@territories.route('/get_constraints')
def get_constraints():
    original_graph = NXGraph(width, height)
    c_l_d = v.get_linear_constraints_dict()
    if detection:
        original_graph.nx_g = GraphGenerator.convert2nx(GraphImporter.add_attributes(orig, g))
    else:
        original_graph.nx_g = g.copy()
    original_graph.reduce_graph(c_l_d)
    return original_graph.get_constraints_nodes(c_l_d)


@territories.route('/get_detailed_info')
def get_detailed_info():
    original_graph = NXGraph(width, height)
    if detection:
        original_graph.nx_g = GraphGenerator.convert2nx(GraphImporter.add_attributes(orig, g))
    else:
        original_graph.nx_g = g.copy()
    return original_graph.get_detailed_info()


@territories.route('/get_cluster_attr')
def get_cluster_attr():
    res = {}
    res["cluster_name"] = {}
    res["cluster_quality"] = {}
    for n in clustered_graph.nx_g.nodes():
        if "cluster-name" in clustered_graph.nx_g.node[n]:
            res["cluster_name"][n] = clustered_graph.nx_g.node[n]["cluster-name"]
        if "quality" in clustered_graph.nx_g.node[n]:
            res["cluster_quality"][n] = clustered_graph.nx_g.node[n]["quality"]
    return json.dumps(res)


@territories.route('/get_original')
def get_original():
    original_graph = NXGraph(width, height)
    if detection:
        original_graph.nx_g = GraphGenerator.convert2nx(GraphImporter.add_attributes(orig, g))
    else:
        original_graph.nx_g = g.copy()
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(1, c_l_d, c_p_d)
    return NXGraph.to_json(original_graph.nx_g)
