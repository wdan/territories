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

    def __init__(self, g_type="all", width=1000, height=1000):
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

    def reduce_graph(self, rate, c_l_d, c_p_d):
        self.cal_degree()
        (inner_nodes_dict, outer_nodes_dict) = self.adjust_nodes(rate)
        (inner_edges_dict, outer_edges_dict) = self.adjust_edges()
        self.cal_outer_positions(outer_nodes_dict, outer_edges_dict, c_l_d)
        self.cal_inner_positions(inner_nodes_dict, inner_edges_dict, c_p_d)

    def init_d_cluster(self):
        self.nx_g.clear()
        self.import_cluster_nodes()
        self.import_cluster_edges()

    def init_r_cluster(self):
        generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
        self.nx_g = generator.get_nx()
        #g = generator.get_ig()
        #cv = generator.community_detection(g)
        #original_graph = generator.get_nx()
        #clustered_graph = generator.convert2nx(cv)

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

    def cal_inner_positions(self, inner_nodes_dict, inner_edges_dict, constraints_dict):
        p = ForceDirectedLayout.cal_rd_layout(inner_nodes_dict, inner_edges_dict, constraints_dict)
        for i, e in enumerate(inner_nodes_dict.keys()):
            if e in p:
                self.nx_g.node[e]["x"] = p[e]["x"]
                self.nx_g.node[e]["y"] = p[e]["y"]

    def cal_outer_positions(self, outer_nodes_dict, outer_edges_dict, constraints_dict):
        p = ForceDirectedLayout.cal_fd_layout(outer_nodes_dict, outer_edges_dict,
                                              self.width, self.height, constraints_dict)
        for i, e in enumerate(outer_nodes_dict.keys()):
            if e in p:
                self.nx_g.node[e]["x"] = p[e]["x"]
                self.nx_g.node[e]["y"] = p[e]["y"]
                self.nx_g.node[e]["visible"] = 1
            else:
                self.nx_g.node[e]["visible"] = 0
        for i, e in enumerate(outer_edges_dict.keys()):
            cluster1 = self.nx_g.node[e[0]]["cluster"]
            cluster2 = self.nx_g.node[e[1]]["cluster"]
            if ((cluster1, cluster2) in constraints_dict) and e[0] in p and e[1] in p:
                self.nx_g.edge[e[0]][e[1]]["visible"] = 1
            else:
                self.nx_g.edge[e[0]][e[1]]["visible"] = 0

    def cal_cluster_voronoi_positions(self):
        self.cal_mds_positions()
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
                self.nx_g.node[e]["external"] = 0
                self.nx_g.node[e]["visible"] = 1
                if outdegree > 0:
                    self.nx_g.node[e]["external"] = 1
                    cluster_max = 0
                    tgt_cluster = -1
                    for cluster_key in tgt_cluster_edge_num_dict.keys():
                        if cluster_max < tgt_cluster_edge_num_dict[cluster_key]:
                            cluster_max = tgt_cluster_edge_num_dict[cluster_key]
                            tgt_cluster = cluster_key
                    self.nx_g.node[e]["tgt_cluster"] = tgt_cluster

    def adjust_nodes(self, rate):
        outer_nodes_dict = {}
        inner_nodes_dict = {}
        for e in self.nx_g.nodes():
            if self.nx_g.node[e]["external"] == 1 and self.nx_g.node[e]["out_degree"] > self.ADJUST_NUMBER:
                outer_nodes_dict[e] = self.nx_g.node[e]
            elif self.nx_g.node[e]["external"] == 0:
                inner_nodes_dict[e] = self.nx_g.node[e]
        sorted_o_f_n = sorted(outer_nodes_dict.items(), key=lambda (k, v): v["out_degree"])
        for e in sorted_o_f_n:
            self.nx_g.node[e[0]]["visible"] = 0
        sorted_o_f_n = sorted_o_f_n[-int(len(sorted_o_f_n) * rate):]
        sorted_o_f_n = dict(sorted_o_f_n)
        sorted_i_f_n = inner_nodes_dict
        return (sorted_i_f_n, sorted_o_f_n)

    def adjust_edges(self):
        inner_edges_dict = {}
        outer_edges_dict = {}
        for e in self.nx_g.edges():
            num0 = self.nx_g.node[e[0]]["out_degree"]
            num1 = self.nx_g.node[e[1]]["out_degree"]
            src_cluster0 = self.nx_g.node[e[0]]["cluster"]
            src_cluster1 = self.nx_g.node[e[1]]["cluster"]
            if num0 > 0 and num1 > 0:
                if (num0 > self.ADJUST_NUMBER and num1 > self.ADJUST_NUMBER):
                    tgt_cluster0 = self.nx_g.node[e[0]]["tgt_cluster"]
                    tgt_cluster1 = self.nx_g.node[e[1]]["tgt_cluster"]
                    if src_cluster0 == tgt_cluster1 and src_cluster1 == tgt_cluster0:
                        self.nx_g.edge[e[0]][e[1]]["visible"] = 1
                        outer_edges_dict[(e[0], e[1])] = self.nx_g.edge[e[0]][e[1]]
                    else:
                        self.nx_g.edge[e[0]][e[1]]["visible"] = 0
            else:
                self.nx_g.edge[e[0]][e[1]]["visible"] = 0
                inner_edges_dict[(e[0], e[1])] = self.nx_g.edge[e[0]][e[1]]
        return (inner_edges_dict, outer_edges_dict)

    @classmethod
    def to_json(cls, g):
        return json_graph.dumps(g)
