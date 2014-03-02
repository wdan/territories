# -*- coding: utf-8 -*-

import networkx as nx
import igraph as ig
from networkx.readwrite import json_graph


class Graph(object):

    def __init__(self):
        self.nx_g = nx.Graph()
        self.igraph_g = ig.Graph()
        #self.init_all()
        self.init_all_igraph()
        #self.init_cluster()

    def init_all_igraph(self):
        self.import_igraph_nodes()
        self.import_igraph_edges()
        self.import_igraph_communities()

    def import_igraph_nodes(self):
        self.node_dic = {}
        res = self._import_politicsuk_nodes()
        for i, key in enumerate(res.keys()):
            self.igraph_g.add_vertices(1)
            self.igraph_g.vs[i]["id"] = key
            self.node_dic[key] = i
            attributes = res[key]
            for attr in attributes.keys():
                self.igraph_g.vs[i]["cluster"] = attributes[attr]

    def import_igraph_edges(self):
        res = self._import_politicsuk_edges()
        for e in res:
            src = self.node_dic[e[0]]
            tgt = self.node_dic[e[1]]
            self.igraph_g.add_edges((src, tgt))

    def import_igraph_communities(self):
        res = self._import_politicsuk_communities()
        for key in res.keys():
            self.igraph_g.vs[self.node_dic[key]]["cluster"] = res[key]

    def import_cluster_nodes(self):
        res = self._import_politicsuk_cluster_nodes()
        for i, e in enumerate(res.keys()):
            self.nx_g.add_node(i, size=res[i])

    def _import_politicsuk_cluster_nodes(self):
        communities_file = open("territories/data/politicsuk.communities", "r")
        communities_cnt = {}
        self.item_to_communities = {}
        for i, row in enumerate(communities_file):
            row_entries = row.split(":")
            nodes_id_list = row_entries[1].split(",")
            for e in nodes_id_list:
                self.item_to_communities[int(e)] = i
                if i in communities_cnt:
                    communities_cnt[i] += 1
                else:
                    communities_cnt[i] = 0
        return communities_cnt

    def init_cluster(self):
        self.import_cluster_nodes()
        self.import_cluster_edges()

    def import_cluster_edges(self):
        res = self._import_politicsuk_cluster_edges()
        for key in res.keys():
            attributes = res[key]
            self.nx_g.add_edge(key[0], key[1])
            for attr in attributes.keys():
                self.nx_g.edge[key[0]][key[1]][attr] = attributes[attr]

    def _import_politicsuk_cluster_edges(self):
        dics = {}
        res = {}
        matrix = [[0 for x in xrange(5)] for x in xrange(5)]
        for i in xrange(5):
            for j in xrange(5):
                matrix[i][j] = 0
        edges_file = open("territories/data/politicsuk-follows.mtx", "r")
        for i, row in enumerate(edges_file):
            if i == 0:
                continue
            row_entries = row.split()
            if (int(row_entries[1]), int(row_entries[0])) in dics:
                community1 = self.item_to_communities[int(row_entries[0])]
                community2 = self.item_to_communities[int(row_entries[1])]
                matrix[community1][community2] += 1
            else:
                dics[(int(row_entries[0]), int(row_entries[1]))] = 1

        for i in xrange(5):
            for j in xrange(i+1, 5):
                if (matrix[i][j] + matrix[j][i] > 0):
                    res[(i, j)] = {}
                    res[(i, j)]["weight"] = matrix[i][j] + matrix[j][i]
        return res

    def init_all(self):
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    def import_nodes(self):
        res = self._import_politicsuk_nodes()
        for key in res.keys():
            self.nx_g.add_node(key)
            attributes = res[key]
            for attr in attributes.keys():
                self.nx_g.node[key][attr] = attributes[attr]

    def import_edges(self):
        res = self._import_politicsuk_edges()
        for e in res:
            self.nx_g.add_edge(e[0], e[1])

    def import_communities(self):
        res = self._import_politicsuk_communities()
        for key in res.keys():
            self.nx_g.node[key]["cluster"] = res[key]

    def _import_politicsuk_nodes(self):
        #nodes_file = open("territories/data/politicsuk.ids", "r")
        nodes_file = open("../data/politicsuk.ids", "r")
        res = {}
        for row in nodes_file:
            res[int(row)] = {}
            res[int(row)]["cluster"] = 0
        return res

    def _import_politicsuk_edges(self):
        #edges_file = open("territories/data/politicsuk-retweets.mtx", "r")
        edges_file = open("../data/politicsuk-retweets.mtx", "r")
        dics = {}
        res = []
        for i, row in enumerate(edges_file):
            if i == 0:
                continue
            row_entries = row.split()
            if (int(row_entries[1]), int(row_entries[0])) in dics:
                res.append((int(row_entries[0]), int(row_entries[1])))
            else:
                dics[(int(row_entries[0]), int(row_entries[1]))] = 1
        return res

    def _import_politicsuk_communities(self):
        #communities_file = open("territories/data/politicsuk.communities", "r")
        communities_file = open("../data/politicsuk.communities", "r")
        res = {}
        for i, row in enumerate(communities_file):
            row_entries = row.split(":")
            nodes_id_list = row_entries[1].split(",")
            for e in nodes_id_list:
                res[int(e)] = i + 1
        return res

    def to_json(self):
        return json_graph.dumps(self.nx_g)


if __name__ == "__main__":
    graph = Graph()
    g = graph.igraph_g
    layout = g.layout("fr")
    color_dict = {0: "blue", 1: "pink", 2: "green", 3: "yellow", 4: "red", 5: "purple"}
    visual_style = {}
    visual_style["vertex_size"] = 10
    visual_style["vertex_color"] = [color_dict[e] for e in g.vs["cluster"]]
    visual_style["layout"] = layout
    ig.plot(g, **visual_style)
