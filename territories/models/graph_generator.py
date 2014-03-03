__author__ = 'wenbin'

from random import randint
import networkx as nx
import igraph as ig


class GraphGenerator(object):
    # com stands for community
    # PR stands for probability
    def __init__(self, num_com, num_in_com, edge_pr_in_com=0.6,
                 edge_pr_btw_com=0.05):
        self._ig = ig.Graph()
        self._nx = nx.Graph()
        n_c = num_com
        n_in_c = num_in_com
        p_in_c = edge_pr_in_com
        p_btw_c = edge_pr_btw_com

        for i in xrange(n_c):
            self._ig += ig.Graph.GRG(n_in_c, p_in_c)

        for i in xrange(n_c):
            seq = self._ig.vs.select(lambda v: v.index >= i * n_in_c
                                     and v.index < (i+1) * n_in_c)
            for v in seq:
                v["cluster"] = i

        for f in xrange(n_c - 1):
            for t in range(f + 1, n_c):
                for j in xrange(int((n_in_c * (n_in_c - 1) / 2) * p_btw_c)):
                    self._ig.add_edge(randint(f * n_in_c, (f + 1) * n_in_c - 1),
                                      randint(t * n_in_c, (t + 1) * n_in_c - 1))

    def get_ig(self):
        return self._ig

    def get_nx(self):
        self.__convert2nx__()
        return self._nx

    def plot_ig(self):
        layout = self._ig.layout("kk")
        ig.plot(self._ig, layout=layout)

    def __convert2nx__(self):
        g = self._ig
        vertex_seq = g.vs.select()

        for v in vertex_seq:
            self._nx.add_node(v.index, cluster=v["cluster"])
        for e in g.es:
            self._nx.add_edge(*e.tuple)


if __name__ == '__main__':
    generator = GraphGenerator(4, 20)
    # generator.plot_ig()
    g = generator.get_nx()


