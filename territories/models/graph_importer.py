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

    def get_school(self):
        g = ig.load("territories/data/data_school_day_1.gml")
        g.simplify(loops=False)
        return g

    def get_football(self):
        g = ig.load("territories/data/football.gml")
        g.simplify(loops=False)
        return g

    def get_hugo(self):
        g = ig.load("territories/data/lesmis.gml")
        g.simplify(loops=False)
        return g

    def get_books(self):
        g = ig.load("territories/data/polbooks.gml")
        g.simplify(loops=False)
        return g

    def get_dblp(self, venue_list):
        #g = ig.load("territories/data/dblp.net")
        #g.simplify(loops=False)
        #return g
        g = ig.Graph.Read_Pajek('territories/data/dblp-all.net')
        data = sio.loadmat('territories/data/dblp.mat')
        return self.generate_sub(g, data, venue_list)

    def get_dblp_paper(self, venueIDList):
        g = ig.Graph()
        data = sio.loadmat('territories/data/dblp.mat')
        paper_venue = data['paper_venue']
        paper_author = data['paper_author'].tocsr()
        author_paper = data['paper_author'].tocsc()
        paper_name = data['paper_name']

        paper_list = {}
        for venue in venueIDList:
            paper_list[venue] = []

        n = paper_venue.size
        paper_id_dict = {}
        id_paper_dict = {}
        paper_venue_dict = {}
        count = 0
        for i in xrange(n):
            v = paper_venue[i][0]
            if v in paper_list:
                paper_id_dict[i] = count
                id_paper_dict[count] = i
                paper_venue_dict[count] = int(v)
                count += 1
                paper_list[int(v)].append(i)

        g.add_vertices(len(paper_id_dict))

        for v in g.vs:
            v['class'] = paper_venue_dict[v.index]
            v['paper_name'] = str(paper_name[id_paper_dict[v.index]][0][0])

        author_list = set()
        for paper_id in paper_id_dict.keys():
            cols = paper_author.getrow(paper_id).nonzero()[1]
            for i in cols:
                author_list.add(i)

        author_list = list(author_list)

        for author_id in author_list:
            rows = author_paper.getcol(author_id).nonzero()[0]
            l = [(paper_id_dict[i], paper_id_dict[j]) for i in rows for j in rows if i>j and i in paper_id_dict and j in paper_id_dict]
            if len(l) > 0:
                g.add_edges(l)

        g.simplify(loops=False)

        return g

    def get_dblp_os(self):
        return self.get_dblp([853, 1074, 1615, 1451, 890])

    def get_dblp_os_paper(self):
        return self.get_dblp_paper([853, 1074, 1615, 1451, 890])

    def get_dblp_vis_paper(self):
        return self.get_dblp_paper([2308, 1984, 1512, 3078, 2960])

    def get_dblp_theory(self):
        return self.get_dblp([1082, 758, 1069, 1305, 1480])

    def get_dblp_sub(self, g, rate):
#        veq = g.vs.select(_degree_gt = (1 - rate) * g.maxdegree())
        veq = g.vs.select(_degree_gt=10)
        return g.induced_subgraph(veq)

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

    def generate_sub(self, g, data, venueIDList):

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

    @classmethod
    def add_attributes(cls, orig, g):
        for attr in orig.vertex_attributes():
            for v in orig.vs:
                g.vs[v.index][attr] = v[attr]
        for attr in orig.edge_attributes():
            for e in orig.es:
                g.es[e.index][attr] = e[attr]
        return g
