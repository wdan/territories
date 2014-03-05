# -*- coding: utf-8 -*-

import json

from polygon import Polygon


class Voronoi(object):

    def __init__(self, data):
        data = json.loads(data)
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
            cluster_id = self.mid_points[i]["cluster"]
            for point in e:
                x = point["x"]
                y = point["y"]
                if (x, y) not in self.point_cluster_dict:
                    self.point_cluster_dict[(x, y)] = []
                self.point_cluster_dict[(x, y)].append(cluster_id)
        for i, e in enumerate(data["polygons"]):
            p = Polygon(self.mid_points[i]["cluster"])
            for j, point in enumerate(e):
                if j == 0:
                    px = point["x"]
                    py = point["y"]
                    continue
                x = point["x"]
                y = point["y"]
                setA = set(self.point_cluster_dict[(px, py)])
                setB = set(self.point_cluster_dict[(x, y)])
                setSelf = set([self.mid_points[i]["cluster"]])
                s = setA & setB - setSelf
                p.add_edge(px, py, x, y, s)
                px = x
                py = y
            x = e[0]["x"]
            y = e[0]["y"]
            setA = set(self.point_cluster_dict[(px, py)])
            setB = set(self.point_cluster_dict[(x, y)])
            setSelf = set([self.mid_points[i]["cluster"]])
            s = setA & setB - setSelf
            p.add_edge(px, py, x, y, s)
            self.polygons.append(p)

        print len(self.polygons)
        for i, p in enumerate(self.polygons):
            print "Polygon" + str(p.cluster) + ":"
            for i, e in enumerate(p.edge_list):
                print "Edge " + str(i) + ": x1:" + str(e["x1"]) + ", y1:" + str(e["y1"]) + ", x2:" + str(e["x2"]) + ", y2:" + str(e["y2"]) + ", tgt_cluster:" + str(e["tgt_cluster"])
