__author__ = 'wenbin'

from random import randint
import networkx as nx
import igraph as ig


class GraphGenerator(object):
    # com stands for community
    # PR stands for probability
    def __init__(self, num_com, num_in_com, edge_pr_in_com=0.8, edge_pr_btw_com=0.05, low=0.6, high=1.2):
        self.__ig__ = ig.Graph()
        n_c = num_com
        n_in_c = num_in_com
        n_list = []
        sum_list = [-1]
        p_in_c = edge_pr_in_com
        p_btw_c = edge_pr_btw_com

        for i in xrange(n_c):
            tmp = randint(int(low*n_in_c), int(high*n_in_c))
            n_list.append(tmp)
            self.__ig__ += ig.Graph.GRG(tmp, p_in_c)
            sum_list.append(sum_list[len(sum_list)-1] + tmp)

        for v in self.__ig__.vs:
            for i in xrange(n_c):
                if v.index <= sum_list[i+1]:
                    v["cluster"] = i
                    break

        for f in xrange(n_c - 1):
            for t in range(f + 1, n_c):
                flag = randint(0, 100)
                if flag > 60:
                    for j in xrange(int((n_list[f] * n_list[t] / 2.0) * p_btw_c)):
                        self.__ig__.add_edge(randint(sum_list[f+1] - n_list[f] + 1, sum_list[f+1]),
                                            randint(sum_list[t+1] - n_list[t] + 1, sum_list[t+1]))

        self.__ig__.simplify(loops=False)

        for e in self.__ig__.es:
            e["weight"] = 1

        for v in self.__ig__.vs:
            v["size"] = 1

    def community_detection(self, g):
        cl = g.community_fastgreedy()
        cv = cl.as_clustering()
        cluster_graph = cv.cluster_graph(combine_edges='sum', combine_vertices='sum')
        return self.convert2nx(cluster_graph)

    def get_ig(self):
        return self.__ig__

    def get_nx(self):
        return self.convert2nx(self.__ig__)

    def plot_ig(self, g):
        layout = g.layout("kk")
        ig.plot(g, layout=layout)

    def convert2nx(self, g):

        nx_graph = nx.Graph()
        vertex_seq = g.vs.select()

        for v in vertex_seq:
            nx_graph.add_node(v.index)
            for attr in g.vertex_attributes():
                nx_graph.node[v.index][attr] = v[attr]
        for e in g.es:
            nx_graph.add_edge(*e.tuple)
            for attr in g.edge_attributes():
                nx_graph[e.source][e.target][attr] = e[attr]

        return nx_graph

if __name__ == '__main__':
    generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02)
    generator.plot_ig(generator.get_ig())
    g = generator.get_nx()
    print g
    cv = generator.community_detection(generator.get_ig())

    generator.plot_ig(cv)
    for v in cv.vs:
        print v["size"]
