# -*- coding: utf-8 -*-

import json

from polygon import Polygon

from constraint import Constraint


class Voronoi(object):

    def __init__(self, data, shrink):
        data = json.loads(data)
        self.polygons = []
        self.point_cluster_dict = {}
        for n in data["nodes"]:
            self.polygons.append(Polygon(n["cluster"], n["x"], n["y"], 0))
        for i, e in enumerate(data["polygons"]):
            cluster_id = self.polygons[i].cluster
            for point in e:
                x = point["x"]
                y = point["y"]
                if (x, y) not in self.point_cluster_dict:
                    self.point_cluster_dict[(x, y)] = []
                self.point_cluster_dict[(x, y)].append(cluster_id)
        for i, e in enumerate(data["polygons"]):
            p = self.polygons[i]
            for j, point in enumerate(e):
                if j == 0:
                    px = point["x"]
                    py = point["y"]
                    continue
                x = point["x"]
                y = point["y"]
                setA = set(self.point_cluster_dict[(px, py)])
                setB = set(self.point_cluster_dict[(x, y)])
                setSelf = set([self.polygons[i].cluster])
                s = setA & setB - setSelf
                p.add_edge(px, py, x, y, s)
                px = x
                py = y
            x = e[0]["x"]
            y = e[0]["y"]
            setA = set(self.point_cluster_dict[(px, py)])
            setB = set(self.point_cluster_dict[(x, y)])
            setSelf = set([self.polygons[i].cluster])
            s = setA & setB - setSelf
            p.add_edge(px, py, x, y, s)

        #print len(self.polygons)
        #for i, p in enumerate(self.polygons):
            #print "Polygon" + str(p.cluster) + ":"
            #for i, e in enumerate(p.edge_list):
                #print "Edge " + str(i) + ": x1:" + str(e["x1"]) + ", y1:" + str(e["y1"]) + ", x2:" + str(e["x2"]) + ", y2:" + str(e["y2"]) + ", tgt_cluster:" + str(e["tgt_cluster"])
        #from util import inside_polygon
        #for p in self.polygons:
            #mid_p = {"x": p.mid_x, "y": p.mid_y}
            #print inside_polygon(mid_p, p.points)

    def get_linear_constraints_dict(self):
        constraints_dict = {}
        for p in self.polygons:
            cluster_src = p.cluster
            for e in p.edge_list:
                if e["tgt_cluster"] is not None:
                    cluster_tgt = e["tgt_cluster"]
                    c = Constraint(e["x1"], e["y1"], e["x2"], e["y2"],
                                   p.mid_x, p.mid_y)
                    constraints_dict[(cluster_src, cluster_tgt)] = c
        return constraints_dict

    def get_polygon_constraints_dict(self):
        constraints_dict = {}
        for p in self.polygons:
            cluster = p.cluster
            constraints_dict[cluster] = {}
            constraints_dict[cluster]["bounding_box"] = p.get_bounding_box()
            constraints_dict[cluster]["points"] = p.points(10)
        return constraints_dict

    def to_dict(self):
        res = []
        for p in self.polygons:
            res.append(p.to_dict())
        return res

    def to_json(self):
        return json.dumps(self.to_dict())
