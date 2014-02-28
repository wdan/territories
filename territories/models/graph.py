# -*- coding: utf-8 -*-

import networkx as nx
from networkx.readwrite import json_graph


class Graph(object):

    def __init__(self):
        self.nx_g = nx.Graph()
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    def import_nodes(self):
        self._import_politicsuk_nodes()

    def import_edges(self):
        self._import_politicsuk_edges()

    def import_communities(self):
        self._import_politicsuk_communities()

    def _import_politicsuk_nodes(self):
        #nodes_file = open("territories/data/politicsuk.ids", "r")
        nodes_file = open("../data/politicsuk.ids", "r")
        for row in nodes_file:
            self.nx_g.add_node(int(row))
            self.nx_g.node[int(row)]["cluster"] = 0

    def _import_politicsuk_edges(self):
        edges_file = open("../data/politicsuk-follows.mtx", "r")
        for i, row in enumerate(edges_file):
            if i == 0:
                continue
            row_entries = row.split()
            self.nx_g.add_edge(int(row_entries[0]), int(row_entries[1]))

    def _import_politicsuk_communities(self):
        communities_file = open("../data/politicsuk.communities", "r")
        for i, row in enumerate(communities_file):
            row_entries = row.split(":")
            nodes_id_list = row_entries[1].split(",")
            for e in nodes_id_list:
                self.nx_g.node[int(e)]["cluster"] = i + 1

    def to_json(self):
        return json_graph.dumps(self.nx_g)


if __name__ == "__main__":
    graph = Graph()
    print(graph.to_json())
