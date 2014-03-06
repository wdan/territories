# -*- coding: utf-8 -*-

import json
from random import randint

import networkx as nx
from networkx.readwrite import json_graph

from graph import AbstractGraph
from graph_generator import GraphGenerator
from data_politicsuk import PoliticsUK as DataSet
from force_directed import ForceDirectedLayout
from mds import MDSLayout
from util import translate


class NXGraph(AbstractGraph):

    ADJUST_NUMBER = 0
    MAX_SIZE = 1000

    def __init__(self, g_type="all", width=960, height=720):
        self.width = width
        self.height = height
        self.nx_g = nx.Graph()
        if g_type == "r_cluster":
            self.init_r_cluster()
        elif g_type == "d_cluster":
            self.init_d_cluster()
        else:
            self.init_all()

    @property
    def size(self):
        return len(self.nx_g.nodes())

    def init_all(self):
        self.nx_g.clear()
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    def reduce_graph(self, constraints_dict):
        self.cal_degree()
        self.adjust_graph()
        self.cal_force_directed_positions(constraints_dict)

    def init_d_cluster(self):
        self.nx_g.clear()
        self.import_cluster_nodes()
        self.import_cluster_edges()

    def init_r_cluster(self):
        generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
        self.nx_g = generator.get_nx()
        self.nx_g = generator.community_detection(generator.get_ig())

    def cal_mds_positions(self):
        (matrix, m) = self.cal_edge_weight_matrix()
        p = MDSLayout.cal_mds(matrix, m)
        x_min = min(map(lambda e: e[0], p))
        x_max = max(map(lambda e: e[0], p))
        y_min = min(map(lambda e: e[1], p))
        y_max = max(map(lambda e: e[1], p))
        for i, e in enumerate(self.nx_g.nodes()):
            self.nx_g.node[e]["x"] = translate(p[i][0], x_min, x_max,
                                               0, self.width)
            self.nx_g.node[e]["y"] = translate(p[i][1], y_min, y_max,
                                               0, self.height)

    def cal_edge_weight_matrix(self):
        n = self.size
        m = 0
        matrix = [[0 for x in xrange(n)] for x in xrange(n)]
        node_dict = {}
        for i, e in enumerate(self.nx_g.nodes()):
            node_dict[e] = i
        for e in self.nx_g.edges():
            index0 = node_dict[e[0]]
            index1 = node_dict[e[1]]
            weight = self.nx_g.edge[e[0]][e[1]]["weight"]
            matrix[index0][index1] = int(weight)
            matrix[index1][index0] = int(weight)
            if m < weight:
                m = weight
        for i in xrange(n):
            matrix[i][i] = int(m * 1.5)
        return (matrix, int(m * 1.5))

    def cal_force_directed_positions(self, constraints_dict):
        p = ForceDirectedLayout.cal_layout(self.nx_g.nodes(data=True), self.nx_g.edges(),
                                           self.width, self.height, constraints_dict)
        for i, e in enumerate(self.nx_g.nodes()):
            self.nx_g.node[e]["x"] = p[i]["x"]
            self.nx_g.node[e]["y"] = p[i]["y"]

    def cal_cluster_voronoi_positions(self):
        from py4j.java_gateway import JavaGateway
        gateway = JavaGateway(auto_convert=True)
        java_app = gateway.entry_point
        x = []
        y = []
        w = []
        cluster = []
        for n in self.nx_g.nodes():
            if "x" in self.nx_g.node[n]:
                t_x = float(self.nx_g.node[n]["x"])
            else:
                t_x = float(randint(0, self.width))
            if "y" in self.nx_g.node[n]:
                t_y = float(self.nx_g.node[n]["y"])
            else:
                t_y = float(randint(0, self.height))
            if "size" in self.nx_g.node[n]:
                t_w = float(self.nx_g.node[n]["size"])
            else:
                t_w = float(randint(0, self.MAX_SIZE))
            x.append(t_x)
            y.append(t_y)
            w.append(t_w)
            cluster.append(n)
        res = java_app.calVoronoiTreemap(x, y, w, cluster,self.width, self.height)
        return res

    def import_cluster_nodes(self):
        res = DataSet.import_cluster_nodes()
        for i, e in enumerate(res.keys()):
            self.nx_g.add_node(e, size=res[e])

    def import_cluster_edges(self):
        res = DataSet.import_cluster_edges()
        for key in res.keys():
            attributes = res[key]
            self.nx_g.add_edge(key[0], key[1])
            for attr in attributes.keys():
                self.nx_g.edge[key[0]][key[1]][attr] = attributes[attr]

    def import_nodes(self):
        res = DataSet.import_nodes()
        for key in res.keys():
            self.nx_g.add_node(key)
            attributes = res[key]
            for attr in attributes.keys():
                self.nx_g.node[key][attr] = attributes[attr]

    def import_edges(self):
        res = DataSet.import_edges()
        for e in res:
            self.nx_g.add_edge(e[0], e[1])

    def import_communities(self):
        (n, res) = DataSet.import_communities()
        self.nx_g.graph["community-num"] = n
        for key in res.keys():
            self.nx_g.node[key]["cluster"] = res[key]

    def cal_degree(self):
        nodes = self.nx_g.nodes()
        for e in nodes:
            neighbors = self.nx_g.neighbors(e)
            indegree = 0
            outdegree = 0
            tgt_cluster_edge_num_dict = {}
            for neighbor in neighbors:
                if self.nx_g.node[e]["cluster"] == self.nx_g.node[neighbor]["cluster"]:
                    indegree += 1
                else:
                    outdegree += 1
                    tgt_cluster_id = self.nx_g.node[neighbor]["cluster"]
                    if tgt_cluster_id not in tgt_cluster_edge_num_dict:
                        tgt_cluster_edge_num_dict[tgt_cluster_id] = 0
                    tgt_cluster_edge_num_dict[tgt_cluster_id] += 1
            if indegree + outdegree == 0:
                self.nx_g.remove_node(e)
            else:
                self.nx_g.node[e]["in_degree"] = indegree
                self.nx_g.node[e]["out_degree"] = outdegree
                if outdegree > 0:
                    tgt_cluster = max(map(lambda key: tgt_cluster_edge_num_dict[key], tgt_cluster_edge_num_dict.keys()))
                    self.nx_g.node[e]["tgt_cluster"] = tgt_cluster

    def adjust_graph(self):
        self.adjust_nodes()
        self.adjust_edges()

    def adjust_nodes(self):
        #for i in xrange(self.nx_g.graph["community-num"]):
            #self.nx_g.add_node("cluster" + str(i))
            #self.nx_g.node["cluster" + str(i)]["size"] = 0
            #self.nx_g.node["cluster" + str(i)]["cluster"] = i
        for e in self.nx_g.nodes():
            if type(e) is int:
                if self.nx_g.node[e]["out_degree"] > self.ADJUST_NUMBER:
                    self.nx_g.node[e]["size"] = 1
                #else:
                    #cluster = self.nx_g.node[e]["cluster"]
                    #self.nx_g.node["cluster" + str(cluster)]["size"] += 1

    def adjust_edges(self):
        for e in self.nx_g.edges():
            num0 = self.nx_g.node[e[0]]["out_degree"]
            num1 = self.nx_g.node[e[1]]["out_degree"]
            if (num0 > self.ADJUST_NUMBER and num1 > self.ADJUST_NUMBER):
                self.nx_g.edge[e[0]][e[1]]["weight"] = 1
            #elif (num0 > self.ADJUST_NUMBER):
                #cluster_num = self.nx_g.node[e[1]]["cluster"]
                #t_s = "cluster" + str(cluster_num)
                #if self.nx_g.has_edge(t_s, e[0]):
                    #self.nx_g.edge[t_s][e[0]]["weight"] += 1
                #else:
                    #self.nx_g.add_edge(t_s, e[0])
                    #self.nx_g.edge[t_s][e[0]]["weight"] = 1
                #self.nx_g.remove_edge(e[0], e[1])
            #elif (num1 > self.ADJUST_NUMBER):
                #cluster_num = self.nx_g.node[e[0]]["cluster"]
                #t_s = "cluster" + str(cluster_num)
                #if self.nx_g.has_edge(t_s, e[1]):
                    #self.nx_g.edge[t_s][e[1]]["weight"] += 1
                #else:
                    #self.nx_g.add_edge(t_s, e[1])
                    #self.nx_g.edge[t_s][e[1]]["weight"] = 1
                #self.nx_g.remove_edge(e[0], e[1])
            else:
                self.nx_g.remove_edge(e[0], e[1])
        for e in self.nx_g.nodes():
            if (type(e) is int and self.nx_g.node[e]["out_degree"] <=
                    self.ADJUST_NUMBER or self.nx_g.node[e]["size"] == 0):
                self.nx_g.remove_node(e)

    @classmethod
    def to_json(cls, g):
        return json_graph.dumps(g)
