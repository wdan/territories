# -*- coding: utf-8 -*-

import math


class ForceDirectedLayout(object):

    iter_num = 200
    c = 0.5

    @classmethod
    def cal_layout(cls, nodes, edges, width, height, constraints_dict):
        reduced_nodes = []
        reduced_edges = []
        positions = []
        for e in nodes:
            src_cluster = e[1]["cluster"]
            tgt_cluster = e[1]["tgt_cluster"]
            if (src_cluster, tgt_cluster) in constraints_dict:
                reduced_nodes.append(e)
                c = constraints_dict[(src_cluster, tgt_cluster)]
                (t_x, t_y) = c.get_random_coordinate(e[1]["out_degree"])
                positions.append({"x": t_x, "y": t_y})
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
                i_x = positions[i]["x"]
                i_y = positions[i]["y"]
                for j in xrange(n):
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        vector_i_x += float(i_x - j_x) / pow(d, 3) * 1000
                        vector_i_y += float(i_y - j_y) / pow(d, 3) * 1000
                for j in edges_dict[i]:
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        vector_i_x += float(j_x - i_x) / d * math.log(max(d, 1))
                        vector_i_y += float(j_y - i_y) / d * math.log(max(d, 1))
                new_i_x = i_x + vector_i_x * cls.c
                (new_i_x, new_i_y) = c.get_y(degree, new_i_x)
                new_positions.append({"id": reduced_nodes[i][0], "x": new_i_x, "y": new_i_y})
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
