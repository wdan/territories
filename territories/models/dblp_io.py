__author__ = 'wenbin'

import igraph as ig
import scipy.io as sio
# from logger import *


class DBLP(object):
    # @infodecor
    def __init__(self, venueIDList, path, fileName):
        venueIDList.sort()
        self.venueIDList = venueIDList
        self.path = path
        self.fileName = fileName
        self.venueIDString = ''
        for i in self.venueIDList:
            self.venueIDString += str(i) + '_'

        [isFound, graph_str] = self.check_dick()
        if isFound:
            print 'isFound'
            self.g = self.read_graph(graph_str)
        else:
            print 'first'
            self.g = self.generate_graph()

    def generate_graph(self):
        # load dblp.mat
        data = sio.loadmat(self.path+'dblp.mat')
        paper_venue = data['paper_venue']
        paper_author = data['paper_author']
        paper_name = data['paper_name']
        # venue_name = data['venue_name']
        paper_author_csr = paper_author.tocsr()
        author_paper_csc = paper_author.tocsc()

        # parse node
        paper_list = {}
        for venue in self.venueIDList:
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

        g = ig.Graph()
        g.add_vertices(len(paper_id_dict))

        graph_file = open(self.path+self.fileName+'.txt', 'w')
        for v in g.vs:
            # cluster = str(venue_name[paper_venue_dict[v.index]][0][0])
            cluster = paper_venue_dict[v.index]
            label = str(paper_name[id_paper_dict[v.index]][0][0])
            v['class'] = cluster
            v['label'] = label
            graph_file.write(str(v.index)+'\t'+str(cluster)+'\t'+label+'\n')
        graph_file.close()

        self.write_dick()

        author_list = set()
        for paper_id in paper_id_dict.keys():
            cols = paper_author_csr.getrow(paper_id).nonzero()[1]
            for i in cols:
                author_list.add(i)

        author_list = list(author_list)

        for author_id in author_list:
            rows = author_paper_csc.getcol(author_id).nonzero()[0]
            l = [(paper_id_dict[i], paper_id_dict[j]) for i in rows for j in rows if i>j and i in paper_id_dict and j in paper_id_dict]
            if len(l) > 0:
                g.add_edges(l)

        g.simplify(loops=False)
        g.write_pajek(self.path + self.fileName + '.net')
        return g


    def write_dick(self):
        with open(self.path+'dict.txt', 'a') as dict_file:
            dict_file.write(self.venueIDString+'\t'+self.fileName+'\n')
        # dict_file = open(self.path+'dict.txt', 'w')
        # dict_file.write(self.venueIDString+'\t'+self.fileName)
        # dict_file.write('\n')
        # dict_file.flush()
        # dict_file.close()

    def read_graph(self, graph_str):
        try:
            graph_file = open(self.path+graph_str+'.txt')
        except IOError:
            print 'The file '+self.path+graph_str+'.txt'+' does not exist!'
            return None

        g = ig.read(self.path+graph_str+'.net')
        for r in graph_file:
            lines = r.split('\t')
            id = int(lines[0])
            cluster = int(lines[1])
            label = str(lines[2]).rstrip('\n')
            g.vs[id]['class'] = cluster
            g.vs[id]['label'] = label
        graph_file.close()
        return g

    def check_dick(self):
        # try:
        dict_file = open(self.path + 'dict.txt', 'r')
        # except IOError:
        #     dict_file = open(self.path + 'dict.txt', 'w')
        #     dict_file.close()
        #     return [False,'']

        isFound = False
        graph_str = ''
        for r in dict_file:
            line = r.split('\t')
            str_list = line[0]
            graph_str = line[1].rstrip('\n')
            if self.venueIDString == str_list or graph_str == self.fileName:
                isFound = True
                break
        dict_file.close()
        return [isFound, graph_str]

if __name__ == '__main__':
    dblp = DBLP([2308, 1984, 1512, 3078, 2960], '../data/', 'vis_5')
    print dblp.g

