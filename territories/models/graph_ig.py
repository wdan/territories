# -*- coding: utf-8 -*-

import igraph as ig

from graph import AbstractGraph
from politicsuk_data import PoliticsUK


class IGGraph(AbstractGraph):

    def __init__(self):
        self.igraph_g = ig.Graph()
        self.init_all()

    def init_all(self):
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    def import_nodes(self):
        self.node_dic = {}
        res = PoliticsUK.import_nodes()
        for i, key in enumerate(res.keys()):
            self.igraph_g.add_vertices(1)
            self.igraph_g.vs[i]["id"] = key
            self.node_dic[key] = i
            attributes = res[key]
            for attr in attributes.keys():
                self.igraph_g.vs[i]["cluster"] = attributes[attr]

    def import_edges(self):
        res = PoliticsUK.import_edges()
        for e in res:
            src = self.node_dic[e[0]]
            tgt = self.node_dic[e[1]]
            self.igraph_g.add_edges((src, tgt))

    def import_communities(self):
        res = PoliticsUK.import_communities()
        for key in res.keys():
            self.igraph_g.vs[self.node_dic[key]]["cluster"] = res[key]

if __name__ == "__main__":
    graph = IGGraph()
    g = graph.igraph_g
    layout = g.layout("fr")
    color_dict = {0: "blue", 1: "pink", 2: "green", 3: "yellow", 4: "red", 5: "purple"}
    visual_style = {}
    visual_style["vertex_size"] = 10
    visual_style["vertex_color"] = [color_dict[e] for e in g.vs["cluster"]]
    visual_style["layout"] = layout
    ig.plot(g, **visual_style)
