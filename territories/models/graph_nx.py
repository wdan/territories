# -*- coding: utf-8 -*-

import networkx as nx
from networkx.readwrite import json_graph

from graph import AbstractGraph
from politicsuk_data import PoliticsUK


class NXGraph(AbstractGraph):

    def __init__(self, g_type="all"):
        self.nx_g = nx.Graph()
        if g_type == "cluster":
            self.init_cluster()
        else:
            self.init_all()

    def import_cluster_nodes(self):
        res = PoliticsUK.import_cluster_nodes()
        for i, e in enumerate(res.keys()):
            self.nx_g.add_node(i, size=res[i])

    def init_all(self):
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    def init_cluster(self):
        self.import_cluster_nodes()
        self.import_cluster_edges()

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
        res = PoliticsUK.import_communities()
        for key in res.keys():
            self.nx_g.node[key]["cluster"] = res[key]

    def to_json(self):
        return json_graph.dumps(self.nx_g)
