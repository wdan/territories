# -*- coding: utf-8 -*-

import igraph as ig
import scipy.io as sio


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

    def generate_sub(g, data, venueIDList):

        paper_list = {}
        author_list = {}
        for venue in venueIDList:
            paper_list[venue] = []
            author_list[venue] = []

        paper_venue = data['paper_venue']
        paper_author = data['paper_author'].tocsr()

        n = paper_venue.size
        for i in xrange(n):
            v = paper_venue[i][0]
            if v in paper_list:
                paper_list[v].append(i)

        g.vs[0]['class'] = {}
        total_author_list = []
        for venue in paper_list.keys():
            paper = paper_list[venue]
            for ID in paper:
                cols = paper_author.getrow(ID).nonzero()[1]
                author_list[venue] += list(cols)
                total_author_list += list(cols)
                for authorID in cols:
                    authorID = int(authorID)
                    if g.vs[authorID]['class'] is None:
                        g.vs[authorID]['class'] = {}
                    if int(venue) not in g.vs[authorID]['class']:
                        g.vs[authorID]['class'][int(venue)] = 0
                    g.vs[authorID]['class'][int(venue)] += 1

        for venue in paper_list.keys():
            print(str(venue)+": Author nums:")
            print(len(set(author_list[venue])))

        print('Total number:')
        print(len(set(total_author_list)))
        total_author_list = list(set(total_author_list))

        return g.induced_subgraph(total_author_list)

    def get_dblp_os(self):
        g = ig.Graph.Read_Pajek('territories/data/dblp-all.net')
        g.simplify(loops=False)

        data = sio.loadmat('territories/data/dblp.mat')

        return generate_sub(g, data, [853, 1074, 1615, 1451, 890])

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
