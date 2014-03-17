__author__ = 'wenbin'

import igraph as ig
import scipy.io as sio

class DBLP(object):

    def __init__(self, venue_id_list, fileName, type='paper', path='territories/data/dblp/'):

        venue_id_list.sort()
        self.venue_id_list = venue_id_list
        self.path = path
        self.file_name = fileName+'_'+type
        self.venue_id_string = ''

        if type == 'paper':
            for i in self.venue_id_list:
                self.venue_id_string += str(i) + '_'
            [isFound, graph_str] = self.check_dick()
            if isFound:
                self.g = self.read_graph_paper(graph_str)
            else:
                self.g = self.generate_graph_paper()
        else:
            for i in self.venue_id_list:
                self.venue_id_string += str(i) + '*'
            [isFound, graph_str] = self.check_dick()
            if isFound:
                self.g = self.read_graph_author(graph_str)
            else:
                self.g = self.generate_graph_author()

        # self.venue_name = self.read_venue_file()
        # print self.venue_name

    def read_graph_author(self, graph_str):
        try:
            graph_file = open(self.path+graph_str+'.txt')
        except IOError:
            print 'The file '+self.path+graph_str+'.txt'+' does not exist!'
            return None

        g = ig.read(self.path+graph_str+'.net')
        for i, r in enumerate(graph_file):
            if i%2 == 0:
                lines = r.split('\t')
                id = int(lines[0])
                label = str(lines[1]).rstrip('\n')
                g.vs[id]['label'] = label
            else:
                g.vs[id]['class'] = {}
                lines = r.split('\t')
                n = len(lines)
                for j in xrange(n/2):
                    g.vs[id]['class'][str(lines[j*2])] = int(lines[j*2+1])
        graph_file.close()
        return g

    # def read_venue_file(self):
    #     try:
    #         venue_file = open(self.path+self.file_name+'_venue.txt')
    #     except IOError:
    #         print 'The file '+self.path+self.file_name+'_venue.txt'+' does not exist!'
    #         return None
    #
    #     r = {}
    #     for line in venue_file:
    #         words = line.split('\t')
    #         id = int(words[0])
    #         name = str(words[1]).rstrip('\n')
    #         r[id] = name
    #
    #     venue_file.close()
    #     return r

    # def write_venue_file(self, data):
    #     venue_file = open(self.path+self.file_name+'_venue.txt', 'w')
    #     for id in self.venue_id_list:
    #         venue_file.write(str(id)+'\t'+str(data[id-1][0][0])+'\n')
    #     venue_file.close()

    def generate_graph_author(self):
        # load dblp.mat
        data = sio.loadmat(self.path+'dblp.mat')
        paper_venue = data['paper_venue']
        paper_author_csr = data['paper_author'].tocsr()
        author_name = data['author_name']
        venue_name = data['venue_name']

        # self.write_venue_file(venue_name)

        # venueID ---> paper list(paper ID)
        paper_list = {}
        for venue in self.venue_id_list:
            paper_list[venue] = []
        n = paper_venue.size
        for i in xrange(n):
            v = paper_venue[i][0]
            if v in paper_list:
                paper_list[v].append(i)

        # venueID ---> author list(author ID)
        author_list = {}

        # dicts for author ID <--> graph index
        author_id_dict = {}
        id_author_dict = {}
        count = 0
        edge_dict = {}
        class_dict = {}
        for venue, papers in paper_list.items():
            for paper_id in papers:
                cols = paper_author_csr.getrow(paper_id).nonzero()[1]
                for author_id in cols:
                    author_id = int(author_id)
                    if author_id not in author_id_dict:
                        class_dict[author_id] = {}
                        author_id_dict[author_id] = count
                        id_author_dict[count] = author_id
                        count += 1
                    if venue not in class_dict[author_id]:
                        class_dict[author_id][venue] = 1
                    else:
                        class_dict[author_id][venue] += 1

                edge_list = [(i, j) for i in cols for j in cols if i > j]

                for e in edge_list:
                    if e in edge_dict:
                        edge_dict[e] += 1
                    else:
                        edge_dict[e] = 1

        g = ig.Graph()
        g.add_vertices(count)

        graph_file = open(self.path+self.file_name+'.txt', 'w')
        for v in g.vs:
            label = str(author_name[id_author_dict[v.index]][0][0])
            v['label'] = label
            v['class'] = {}
            graph_file.write(str(v.index)+'\t'+label+'\n')
            for venue, count in class_dict[id_author_dict[v.index]].items():
                v['class'][str(venue_name[venue-1][0][0])] = count
                graph_file.write(str(venue_name[venue-1][0][0]) + '\t' + str(count) + '\t')
            graph_file.write('\n')

        graph_file.close()

        edge_list = map(lambda e: (author_id_dict[e[0]], author_id_dict[e[1]]), edge_dict.keys())
        g.add_edges(edge_list)
        self.write_dick()
        g.simplify(loops=False)
        g.write_pajek(self.path + self.file_name + '.net')
        return g

    def generate_graph_paper(self):
        # load dblp.mat
        data = sio.loadmat(self.path+'dblp.mat')
        paper_venue = data['paper_venue']
        paper_author = data['paper_author']
        paper_name = data['paper_name']

        paper_author_csr = paper_author.tocsr()
        author_paper_csc = paper_author.tocsc()
        venue_name = data['venue_name']
        # self.write_venue_file(venue_name)
        # parse node
        paper_list = {}
        for venue in self.venue_id_list:
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

        graph_file = open(self.path+self.file_name+'.txt', 'w')
        for v in g.vs:
            cluster = str(venue_name[paper_venue_dict[v.index]-1][0][0])
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
        g.write_pajek(self.path + self.file_name + '.net')
        return g

    def write_dick(self):
        with open(self.path+'dict.txt', 'a') as dict_file:
            dict_file.write(self.venue_id_string+'\t'+self.file_name+'\n')

    def read_graph_paper(self, graph_str):
        try:
            graph_file = open(self.path+graph_str+'.txt')
        except IOError:
            print 'The file '+self.path+graph_str+'.txt'+' does not exist!'
            return None

        g = ig.read(self.path+graph_str+'.net')
        for r in graph_file:
            lines = r.split('\t')
            id = int(lines[0])
            cluster = str(lines[1])
            label = str(lines[2]).rstrip('\n')
            g.vs[id]['class'] = cluster
            g.vs[id]['label'] = label
        graph_file.close()
        return g

    def check_dick(self):
        try:
            dict_file = open(self.path + 'dict.txt', 'r')
        except IOError:
            dict_file = open(self.path + 'dict.txt', 'w')
            dict_file.close()
            return [False,'']

        isFound = False
        graph_str = ''
        for r in dict_file:
            line = r.split('\t')
            str_list = line[0]
            graph_str = line[1].rstrip('\n')
            if self.venue_id_string == str_list or graph_str == self.file_name:
                isFound = True
                break
        dict_file.close()
        return [isFound, graph_str]

if __name__ == '__main__':
    vis5 = DBLP([2308, 1984, 1512, 3078, 2960], 'vis_5', 'paper')
    print vis5.g.ecount()
    print vis5.g.vcount()
    print vis5.g.vs[0]
    os5 =DBLP([2308, 1984, 1512, 3078, 2960], 'os_5', 'author')
    print os5.g.ecount()
    print os5.g.vcount()
    print os5.g.vs[0]

