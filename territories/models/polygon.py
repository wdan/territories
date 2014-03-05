# -*- coding: utf-8 -*-

import math


class Polygon(object):

    SCALE = 50

    def __init__(self, cluster_id, x, y):
        self.edge_list = []
        self.cluster = cluster_id
        self.mid_x = x
        self.mid_y = y

    def add_edge(self, x1, y1, x2, y2, tgt_cluster_id):
        edge_dict = {}
        (xA, yA) = self.interp(self.mid_x, self.mid_y, x1, y1)
        (xB, yB) = self.interp(self.mid_x, self.mid_y, x2, y2)
        edge_dict["x1"] = xA
        edge_dict["y1"] = yA
        edge_dict["x2"] = xB
        edge_dict["y2"] = yB
        c = None
        for item in tgt_cluster_id:
            c = item
        edge_dict["tgt_cluster"] = c
        self.edge_list.append(edge_dict)

    @classmethod
    def vector_norm(cls, x1, y1, x2, y2):
        v = {}
        v["x"] = x2 - x1
        v["y"] = y2 - y1
        v["length"] = math.sqrt(v["x"] * v["x"] + v["y"] * v["y"])
        v["x"] = v["x"] / v["length"]
        v["y"] = v["y"] / v["length"]
        return v

    @classmethod
    def interp(cls, x1, y1, x2, y2):
        v = cls.vector_norm(x1, y1, x2, y2)
        k = (v["length"] - cls.SCALE) / v["length"]
        x = k * v["length"] * v["x"] + x1
        y = k * v["length"] * v["y"] + y1
        return (x, y)
