# -*- coding: utf-8 -*-

import math
from random import uniform

from util import inside_polygon


class ForceDirectedLayout(object):

    iter_num = 200
    c = 0.5
    dis = 20

    @classmethod
    def cal_rd_layout(cls, nodes, edges, constraints_dict):
        reduced_nodes = []
        for e in nodes:
            if e[1]["external"] == 0:
                reduced_nodes.append(e)
        positions = []
        for e in reduced_nodes:
            d = constraints_dict[e[1]["cluster"]]
            bounding_box = d["bounding_box"]
            points = d["points"]
            t_dict = {}
            t_dict["id"] = e[0]
            x = uniform(bounding_box[0], bounding_box[2])
            y = uniform(bounding_box[1], bounding_box[3])
            while not inside_polygon(x, y, points):
                x = uniform(bounding_box[0], bounding_box[2])
                y = uniform(bounding_box[1], bounding_box[3])
            t_dict["x"] = x
            t_dict["y"] = y
            positions.append(t_dict)
        res = {}
        for p in positions:
            res[p["id"]] = {}
            res[p["id"]]["x"] = p["x"]
            res[p["id"]]["y"] = p["y"]
        return res

    @classmethod
    def cal_fd_layout(cls, nodes, edges, width, height, constraints_dict):
        reduced_nodes = []
        reduced_edges = []
        positions = []
        for e in nodes:
            if e[1]["external"] == 1:
                src_cluster = e[1]["cluster"]
                tgt_cluster = e[1]["tgt_cluster"]
                if (src_cluster, tgt_cluster) in constraints_dict:
                    reduced_nodes.append(e)
                    c = constraints_dict[(src_cluster, tgt_cluster)]
                    (t_x, t_y) = c.get_random_coordinate(e[1]["out_degree"])
                    positions.append({"x": t_x, "y": t_y, "cluster": src_cluster})
        n = len(reduced_nodes)
        node_dict = {}
        edges_dict = {}
        for i, e in enumerate(reduced_nodes):
            node_dict[e[0]] = i
            edges_dict[i] = []

        for i, e in enumerate(edges):
            if e[0] in node_dict and e[1] in node_dict:
                reduced_edges.append((e[0], e[1]))
                src_index = node_dict[e[0]]
                tgt_index = node_dict[e[1]]
                if src_index not in edges_dict:
                    edges_dict[src_index] = []
                edges_dict[src_index].append(tgt_index)
                if tgt_index not in edges_dict:
                    edges_dict[tgt_index] = []
                edges_dict[tgt_index].append(src_index)

        for k in xrange(cls.iter_num):
            new_positions = []
            for i in xrange(n):
                src_cluster = reduced_nodes[i][1]["cluster"]
                tgt_cluster = reduced_nodes[i][1]["tgt_cluster"]
                c = constraints_dict[(src_cluster, tgt_cluster)]
                degree = reduced_nodes[i][1]["out_degree"]
                vector_i_x = 0
                vector_i_y = 0
                i_cluster = positions[i]["cluster"]
                i_x = positions[i]["x"]
                i_y = positions[i]["y"]
                for j in xrange(n):
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        #vector_i_x += float(i_x - j_x) / pow(d, 3) * 1000
                        #vector_i_y += float(i_y - j_y) / pow(d, 3) * 1000
                for j in edges_dict[i]:
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        j_cluster = positions[j]["cluster"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        if i_cluster != j_cluster and (i_cluster, j_cluster) in constraints_dict:
                            vector_i_x += float(j_x - i_x) / d * math.log(max(d - cls.dis, 1))
                            vector_i_y += float(j_y - i_y) / d * math.log(max(d - cls.dis, 1))
                        #else:
                            #vector_i_x += float(i_x - j_x) / d * math.log(max(d - cls.dis, 1))
                            #vector_i_y += float(i_y - j_y) / d * math.log(max(d - cls.dis, 1))
                new_i_x = i_x + vector_i_x * cls.c
                (new_i_x, new_i_y) = c.get_y(degree, new_i_x)
                new_positions.append({"id": reduced_nodes[i][0], "x": new_i_x, "y": new_i_y, "cluster": i_cluster})
            positions = new_positions
        res = {}
        for pos in positions:
            res[pos["id"]] = {}
            res[pos["id"]]["x"] = pos["x"]
            res[pos["id"]]["y"] = pos["y"]
        return res


    @classmethod
    def cal_distance_square(cls, x1, y1, x2, y2):
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

    @classmethod
    def cal_distance(cls, x1, y1, x2, y2):
        return math.sqrt(cls.cal_distance_square(x1, y1, x2, y2))
