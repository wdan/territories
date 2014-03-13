# -*- coding: utf-8 -*-

import igraph as ig


class GraphImporter(object):

    def __init__(self, name):
        self.name = name

    def get_citation(self):
        g = ig.Graph()
        graph_file = open("territories/data/ca-GrQc.txt", "r")
        id2index_dict = {}
        edges = []
        for row in graph_file:
            row_entries = row.split()
            id1 = int(row_entries[0])
            id2 = int(row_entries[1])
            if id1 not in id2index_dict:
                id2index_dict[id1] = len(id2index_dict)
            if id2 not in id2index_dict:
                id2index_dict[id2] = len(id2index_dict)
            index1 = id2index_dict[id1]
            index2 = id2index_dict[id2]
            edges.append((index1, index2))
        g.add_vertices(len(id2index_dict.keys()))
        g.add_edges(edges)
        g.simplify(loops=False)
        for e in g.es:
            e["weight"] = 1
        for v in g.vs:
            v["size"] = 1
        return g

    def get_hugo(self):
        g = ig.load("territories/data/lesmis.gml")
        g.simplify(loops=False)
        return g

    def get_books(self):
        g = ig.load("territories/data/polbooks.gml")
        g.simplify(loops=False)
        return g

    @classmethod
    def remove_attributes(cls, g):
        for attr in g.vertex_attributes():
            del g.vs[attr]
        for attr in g.edge_attributes():
            del g.es[attr]
        for e in g.es:
            e["weight"] = 1
        for v in g.vs:
            v["size"] = 1
        return g

        e.index
        g.es[e.index]

    @classmethod
    def add_attributes(cls, orig, g):
        for attr in orig.vertex_attributes():
            for v in orig.vs:
                g.vs[v.index][attr] = v[attr]
        for attr in orig.edge_attributes():
            for e in orig.es:
                g.es[e.index][attr] = e[attr]
        del g.vs["id"]
        return g
