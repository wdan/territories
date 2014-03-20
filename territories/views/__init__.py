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
cluster_name_dict = {}
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
    global v, clustered_graph
    src = int(request.args.get('src', -1))
    tgt = int(request.args.get('tgt', -1))
    s = clustered_graph.cal_cluster_voronoi_positions(src, tgt)
    v = Voronoi(s)
    return v.to_json()


@territories.route('/get_polygon')
def get_aggregate():
    global detection, orig, g, v, name, rate, generator, clustered_graph, cluster_name_dict
    cluster_name_dict = {}
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
    for n in clustered_graph.nx_g.nodes():
        cluster_id = clustered_graph.nx_g.node[n]["cluster"]
        cluster_name = clustered_graph.nx_g.node[n]["cluster-name"]
        cluster_name_dict[cluster_name] = cluster_id
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


@territories.route('/merge_cluster', methods=["POST"])
def merge_cluster():
    global g, v, clustered_graph, cluster_name_dict
    original_graph = NXGraph(width, height)
    cluster_list = request.form.getlist("cluster_list")
    cluster_list = map(lambda e: int(e), cluster_list)
    pos = request.form.getlist("pos")
    pos_dict = {}
    print pos
    for item in pos:
        row = item.split(",")
        cluster_id = int(row[0])
        x = float(row[1])
        y = float(row[2])
        pos_dict[cluster_id] = {}
        pos_dict[cluster_id]["x"] = x
        pos_dict[cluster_id]["y"] = y

    merge_number = request.form["merge_number"]
    if detection:
        original_graph.nx_g = GraphGenerator.convert2nx(GraphImporter.add_attributes(orig, g))
    else:
        original_graph.nx_g = g.copy()
    merge_cluster_name = "merge" + str(merge_number)
    new_cluster_id = len(cluster_name_dict.keys())
    cluster_name_dict[merge_cluster_name] = new_cluster_id
    original_graph.merge_cluster(cluster_list, merge_cluster_name)
    g = original_graph.nx_g
    x = []
    y = []
    w = []
    cluster = []
    t_x = 0
    t_y = 0
    t_size = 0
    for n in clustered_graph.nx_g.nodes():
        cluster_id = clustered_graph.nx_g.node[n]["cluster"]
        if cluster_id not in cluster_list:
            x.append(pos_dict[cluster_id]["x"])
            y.append(pos_dict[cluster_id]["y"])
            w.append(float(clustered_graph.nx_g.node[n]["size"]))
            cluster.append(clustered_graph.nx_g.node[n]["cluster"])
        else:
            t_x = pos_dict[cluster_id]["x"]
            t_y = pos_dict[cluster_id]["y"]
            t_size += clustered_graph.nx_g.node[n]["size"]
    x.append(float(t_x))
    y.append(float(t_y))
    w.append(float(t_size))
    cluster.append(new_cluster_id)
    clustered_graph.nx_g = NXGraph.mark_community(original_graph.nx_g)
    clustered_graph.modify_cluster_id(cluster_name_dict)
    #s = clustered_graph.cal_cluster_voronoi_positions()
    s = clustered_graph.cal_voronoi_positions(x, y, w, cluster)
    v = Voronoi(s)
    print v.to_json()
    return v.to_json()


@territories.route('/get_cluster_attr')
def get_cluster_attr():
    res = {}
    res["cluster_name"] = {}
    res["cluster_quality"] = {}
    for n in clustered_graph.nx_g.nodes():
        cluster_id = clustered_graph.nx_g.node[n]["cluster"]
        if "cluster-name" in clustered_graph.nx_g.node[n]:
            res["cluster_name"][cluster_id] = clustered_graph.nx_g.node[n]["cluster-name"]
        if "quality" in clustered_graph.nx_g.node[n]:
            res["cluster_quality"][cluster_id] = clustered_graph.nx_g.node[n]["quality"]
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
