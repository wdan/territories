# -*- coding: utf-8 -*-

import math
from random import uniform

from util import inside_polygon


class ForceDirectedLayout(object):

    iter_num = 200
    c = 0.5
    dis = 20

    @classmethod
    def cal_rd_layout(cls, nodes_dict, edges_dict, constraints_dict):
        positions = []
        for e in nodes_dict.keys():
            d = constraints_dict[nodes_dict[e]["cluster"]]
            bounding_box = d["bounding_box"]
            points = d["points"]
            t_dict = {}
            t_dict["id"] = e
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
        for e in nodes.keys():
            src_cluster = nodes[e]["cluster"]
            tgt_cluster = nodes[e]["tgt_cluster"]
            if (src_cluster, tgt_cluster) in constraints_dict:
                reduced_nodes.append((e, nodes[e]))
                c = constraints_dict[(src_cluster, tgt_cluster)]
                (t_x, t_y) = c.get_random_coordinate(nodes[e]["out_degree"])
                positions.append({"x": t_x, "y": t_y, "cluster": src_cluster})
        n = len(reduced_nodes)
        nodes_dict = {}
        edges_dict = {}
        for i, e in enumerate(reduced_nodes):
            nodes_dict[e[0]] = i
            edges_dict[i] = []

        for i, e in enumerate(edges):
            if e[0] in nodes_dict and e[1] in nodes_dict:
                reduced_edges.append((e[0], e[1]))
                src_index = nodes_dict[e[0]]
                tgt_index = nodes_dict[e[1]]
                if src_index not in edges_dict:
                    edges_dict[src_index] = []
                edges_dict[src_index].append(tgt_index)
                if tgt_index not in edges_dict:
                    edges_dict[tgt_index] = []
                edges_dict[tgt_index].append(src_index)

        for k in xrange(cls.iter_num):
            new_positions = []
            for i in xrange(n):
                src_cluster_i = reduced_nodes[i][1]["cluster"]
                tgt_cluster_i = reduced_nodes[i][1]["tgt_cluster"]
                c = constraints_dict[(src_cluster_i, tgt_cluster_i)]
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
                        #vector_i_x += float(i_x - j_x) / pow(d, 3)
                        #vector_i_y += float(i_y - j_y) / pow(d, 3)
                for j in edges_dict[i]:
                    if (i != j):
                        src_cluster_j = reduced_nodes[j][1]["cluster"]
                        tgt_cluster_j = reduced_nodes[j][1]["tgt_cluster"]
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        if src_cluster_j == tgt_cluster_i and src_cluster_i == tgt_cluster_j and (src_cluster_i, tgt_cluster_i) in constraints_dict:
                            vector_i_x += float(j_x - i_x) / d * math.log(max(d - cls.dis, 1))
                            vector_i_y += float(j_y - i_y) / d * math.log(max(d - cls.dis, 1))
                        #else:
                            #vector_i_x += float(i_x - j_x) / d * math.log(max(d - cls.dis, 1))
                            #vector_i_y += float(i_y - j_y) / d * math.log(max(d - cls.dis, 1))
                vector_i_x *= cls.c
                vector_i_y *= cls.c
                (new_i_x, new_i_y) = c.cal_next(degree, i_x, i_y, vector_i_x, vector_i_y)
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
