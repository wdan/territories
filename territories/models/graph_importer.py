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
        del g.vs['id']
        del g.es['value']
        g.simplify(loops=False)
        for e in g.es:
            e["weight"] = 1
        for v in g.vs:
            v["size"] = 1
        return g
