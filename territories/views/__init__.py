# -*- coding: utf-8 -*-

import networkx as nx

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
detection = False


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
    global detection, orig, g, v, name, rate, generator
    name = request.args.get('name', 'random')
    width = int(request.args.get('width', 1000))
    height = int(request.args.get('height', 1000))
    shrink = int(request.args.get('shrink', 50))
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
    elif name == "school":
        orig = GraphImporter("").get_school()
        del orig.vs["id"]
    elif name == "dblp":
        orig = GraphImporter("").get_dblp_os()
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
    v = Voronoi(s, shrink)
    return v.to_json()


@territories.route('/get_original')
def get_original():
    original_graph = NXGraph(width, height)
    if detection:
        original_graph.nx_g = GraphGenerator.convert2nx(GraphImporter.add_attributes(orig, g))
    else:
        original_graph.nx_g = g
    c_l_d = v.get_linear_constraints_dict()
    c_p_d = v.get_polygon_constraints_dict()
    original_graph.reduce_graph(rate, c_l_d, c_p_d)
    return NXGraph.to_json(original_graph.nx_g)
