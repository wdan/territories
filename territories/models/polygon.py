# -*- coding: utf-8 -*-

import sys
from util import interp, rotate


class Polygon(object):

    SCALE = 50

    def __init__(self, cluster_id, x, y):
        self.edge_list = []
        self.cluster = cluster_id
        self.mid_x = x
        self.mid_y = y

    def add_edge(self, x1, y1, x2, y2, tgt_cluster_id):
        edge_dict = {}
        (xA, yA) = interp(self.mid_x, self.mid_y, x1, y1, self.SCALE)
        (xB, yB) = interp(self.mid_x, self.mid_y, x2, y2, self.SCALE)
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
        dict_res["points"] = self.points
        area = self.get_width_and_height()
        dict_res["width"] = area[0]
        dict_res["height"] = area[1]
        return dict_res

    @property
    def points(self):
        points = []
        min_y = sys.maxint
        index = -1
        self.edge_list.reverse()
        for i, e in enumerate(self.edge_list):
            if e["y1"] < min_y:
                min_y = e["y1"]
                index = i
        self.edge_list = rotate(self.edge_list, index)
        for e in self.edge_list:
            points.append({"x": e["x1"], "y": e["y1"]})
        return points

    def get_width_and_height(self):
        (min_x, min_y, max_x, max_y) = self.get_bounding_box()
        return (max_x - min_x, max_y - min_y)

    def get_bounding_box(self):
        min_x, max_x = sys.maxint, 1 - sys.maxint
        min_y, max_y = min_x, max_x
        for p in self.points:
            if p["x"] > max_x:
                max_x = p["x"]
            if p["x"] < min_x:
                min_x = p["x"]
            if p["y"] > max_y:
                max_y = p["y"]
            if p["y"] < min_y:
                min_y = p["y"]
        return (min_x, min_y, max_x, max_y)
