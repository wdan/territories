# -*- coding: utf-8 -*-

from util import interp


class Polygon(object):

    def __init__(self, cluster_id, x, y):
        self.edge_list = []
        self.cluster = cluster_id
        self.mid_x = x
        self.mid_y = y

    def add_edge(self, x1, y1, x2, y2, tgt_cluster_id):
        edge_dict = {}
        (xA, yA) = interp(self.mid_x, self.mid_y, x1, y1, 50)
        (xB, yB) = interp(self.mid_x, self.mid_y, x2, y2, 50)
        edge_dict["x1"] = xA
        edge_dict["y1"] = yA
        edge_dict["x2"] = xB
        edge_dict["y2"] = yB
        c = None
        for item in tgt_cluster_id:
            c = item
        edge_dict["tgt_cluster"] = c
        self.edge_list.append(edge_dict)


    def to_dict(self):
        dict_res = {}
        dict_res["cluster"] = self.cluster
        dict_res["mid_x"] = self.mid_x
        dict_res["mid_y"] = self.mid_y
        dict_res["points"] = []
        for e in self.edge_list:
            dict_res["points"].append({"x": e["x1"], "y": e["y1"]})
        return dict_res
