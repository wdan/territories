# -*- coding: utf-8 -*-


class Polygon(object):

    def __init__(self, cluster_id):
        self.edge_list = []
        self.cluster = cluster_id

    def add_edge(self, x1, y1, x2, y2, tgt_cluster_id):
        edge_dict = {}
        edge_dict["x1"] = x1
        edge_dict["y1"] = y1
        edge_dict["x2"] = x2
        edge_dict["y2"] = y2
        c = None
        for item in tgt_cluster_id:
            c = item
        edge_dict["tgt_cluster"] = c
        self.edge_list.append(edge_dict)
