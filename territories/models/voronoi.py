# -*- coding: utf-8 -*-

import json

from polygon import Polygon


class Voronoi(object):

    def __init__(self, data):
        data = json.loads(data)
        self.polygons = []
        self.point_cluster_dict = {}
        for n in data["nodes"]:
            self.polygons.append(Polygon(n["cluster"], n["x"], n["y"]))
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

    def get_constraints_dict(self):
        constraints_dict = {}
        for p in self.polygons:
            cluster_src = p.cluster
            for e in p.edge_list:
                if e["tgt_cluster"] is not None:
                    cluster_tgt = e["tgt_cluster"]
                    constraints_item = {}
                    constraints_item["x1"] = e["x1"]
                    constraints_item["y1"] = e["y1"]
                    constraints_item["x2"] = e["x2"]
                    constraints_item["y2"] = e["y2"]
                    constraints_dict[(cluster_src, cluster_tgt)] = constraints_item
        return constraints_dict

    def to_json(self):
            js_res = []
            for p in self.polygons:
                js_res.append(p.to_dict())
            return json.dumps(js_res)
