# -*- coding: utf-8 -*-

from polygon import Polygon


class Voronoi(object):

    def __init__(self, data):
        self.mid_points = []
        self.polygons = []
        self.point_cluster_dict = {}

        for n in data["nodes"]:
            mid_point_dict = {}
            mid_point_dict["x"] = n["x"]
            mid_point_dict["y"] = n["y"]
            mid_point_dict["cluster"] = n["cluster"]
            self.mid_points.append(mid_point_dict)
        for i, e in enumerate(data["polygons"]):
            p = Polygon()
            for point in e:
                x = point["x"]
                y = point["y"]
                cluster_id = self.mid_points[i]["cluster"]
                if (x, y) not in self.point_cluster_dict:
                    self.point_cluster_dict[(x, y)] = []
                self.point_cluster_dict[(x, y)].append(cluster_id)
