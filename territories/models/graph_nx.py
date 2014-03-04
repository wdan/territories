# -*- coding: utf-8 -*-

from sets import Set

import networkx as nx
from networkx.readwrite import json_graph

from graph import AbstractGraph
from data_politicsuk import PoliticsUK
from force_directed import ForceDirectedLayout


class NXGraph(AbstractGraph):

    ADJUST_NUMBER = 1

    def __init__(self, g_type="all"):
        self.nx_g = nx.Graph()
        if g_type == "cluster":
            self.init_cluster()
        else:
            self.init_all()

    def init_all(self):
        self.import_nodes()
        self.import_edges()
        self.import_communities()
        self.cal_degree()
        p = ForceDirectedLayout.cal_layout(self.nx_g.nodes(), self.nx_g.edges(),
                                           1000, 1000)
        for i, e in enumerate(self.nx_g.nodes()):
            self.nx_g.node[e]["x"] = p[i]["x"]
            self.nx_g.node[e]["y"] = p[i]["y"]

    def init_cluster(self):
        self.import_cluster_nodes()
        self.import_cluster_edges()

    def import_cluster_nodes(self):
        res = PoliticsUK.import_cluster_nodes()
        for i, e in enumerate(res.keys()):
            self.nx_g.add_node(i, size=res[i])

    def import_cluster_edges(self):
        res = PoliticsUK.import_cluster_edges()
        for key in res.keys():
            attributes = res[key]
            self.nx_g.add_edge(key[0], key[1])
            for attr in attributes.keys():
                self.nx_g.edge[key[0]][key[1]][attr] = attributes[attr]

    def import_nodes(self):
        res = PoliticsUK.import_nodes()
        for key in res.keys():
            self.nx_g.add_node(key)
            attributes = res[key]
            for attr in attributes.keys():
                self.nx_g.node[key][attr] = attributes[attr]

    def import_edges(self):
        res = PoliticsUK.import_edges()
        for e in res:
            self.nx_g.add_edge(e[0], e[1])

    def import_communities(self):
        (n, res) = PoliticsUK.import_communities()
        self.nx_g.graph["community-num"] = n
        for key in res.keys():
            self.nx_g.node[key]["cluster"] = res[key]

    def cal_degree(self):
        nodes = self.nx_g.nodes()
        for e in nodes:
            neighbors = self.nx_g.neighbors(e)
            indegree = 0
            outdegree = 0
            for neighbor in neighbors:
                if self.nx_g.node[e]["cluster"] == self.nx_g.node[neighbor]["cluster"]:
                    indegree += 1
                else:
                    outdegree += 1
            if indegree + outdegree == 0:
                self.nx_g.remove_node(e)
            else:
                self.nx_g.node[e]["in_degree"] = indegree
                self.nx_g.node[e]["out_degree"] = outdegree

    def adjust_graph(self):
        self.adjust_nodes()
        self.adjust_edges()

    def adjust_nodes(self):
        for i in xrange(self.nx_g.graph["community-num"]):
            self.nx_g.add_node("cluster" + str(i))
            self.nx_g.node["cluster" + str(i)]["size"] = 0
            self.nx_g.node["cluster" + str(i)]["cluster"] = i
        for e in self.nx_g.nodes():
            if type(e) is int:
                if self.nx_g.node[e]["out_degree"] > self.ADJUST_NUMBER:
                    self.nx_g.node[e]["size"] = 1
                else:
                    cluster = self.nx_g.node[e]["cluster"]
                    self.nx_g.node["cluster" + str(cluster)]["size"] += 1

    def adjust_edges(self):
        for e in self.nx_g.edges():
            num0 = self.nx_g.node[e[0]]["out_degree"]
            num1 = self.nx_g.node[e[1]]["out_degree"]
            if (num0 > self.ADJUST_NUMBER and num1 > self.ADJUST_NUMBER):
                self.nx_g.edge[e[0]][e[1]]["weight"] = 1
            elif (num0 > self.ADJUST_NUMBER):
                cluster_num = self.nx_g.node[e[1]]["cluster"]
                t_s = "cluster" + str(cluster_num)
                if self.nx_g.has_edge(t_s, e[0]):
                    self.nx_g.edge[t_s][e[0]]["weight"] += 1
                else:
                    self.nx_g.add_edge(t_s, e[0])
                    self.nx_g.edge[t_s][e[0]]["weight"] = 1
                self.nx_g.remove_edge(e[0], e[1])
            elif (num1 > self.ADJUST_NUMBER):
                cluster_num = self.nx_g.node[e[0]]["cluster"]
                t_s = "cluster" + str(cluster_num)
                if self.nx_g.has_edge(t_s, e[1]):
                    self.nx_g.edge[t_s][e[1]]["weight"] += 1
                else:
                    self.nx_g.add_edge(t_s, e[1])
                    self.nx_g.edge[t_s][e[1]]["weight"] = 1
                self.nx_g.remove_edge(e[0], e[1])
            else:
                self.nx_g.remove_edge(e[0], e[1])
        for e in self.nx_g.nodes():
            if type(e) is int and self.nx_g.node[e]["out_degree"] <= self.ADJUST_NUMBER or self.nx_g.node[e]["size"] == 0:
                self.nx_g.remove_node(e)

    @classmethod
    def to_json(cls, g):
        return json_graph.dumps(g)
