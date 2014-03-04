# -*- coding: utf-8 -*-

from random import randint
import math


class ForceDirectedLayout(object):

    iter_num = 100
    c = 0.5

    @classmethod
    def cal_layout(cls, nodes, edges, width, height):
        print "Hello"
        n = len(nodes)
        positions = []
        for i in xrange(n):
            positions.append({"x": randint(0, width), "y": randint(0, height)})
        node_dict = {}
        for i, e in enumerate(nodes):
            node_dict[e] = i
        edges_dict = {}
        for i, e in enumerate(edges):
            src_index = node_dict[e[0]]
            tgt_index = node_dict[e[1]]
            if not edges_dict.has_key(src_index):
                edges_dict[src_index] = []
            edges_dict[src_index].append(tgt_index)
            if not edges_dict.has_key(tgt_index):
                edges_dict[tgt_index] = []
            edges_dict[tgt_index].append(src_index)
        for k in xrange(cls.iter_num):
            new_positions = []
            for i in xrange(n):
                vector_i_x = 0
                vector_i_y = 0
                i_x = positions[i]["x"]
                i_y = positions[i]["y"]
                for j in xrange(n):
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        vector_i_x += float(i_x - j_x) / pow(d, 3) * 100
                        vector_i_y += float(i_y - j_y) / pow(d, 3) * 100
                for j in edges_dict[i]:
                    if (i != j):
                        j_x = positions[j]["x"]
                        j_y = positions[j]["y"]
                        d = cls.cal_distance(i_x, i_y, j_x, j_y)
                        vector_i_x += float(j_x - i_x) / d * math.log(max(d, 1))
                        vector_i_y += float(j_y - i_y) / d * math.log(max(d, 1))
                new_i_x = i_x + vector_i_x * cls.c
                new_i_y = i_y + vector_i_y * cls.c
                new_positions.append({"x": new_i_x, "y": new_i_y})
            positions = new_positions
        return positions

    @classmethod
    def cal_distance_square(cls, x1, y1, x2, y2):
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

    @classmethod
    def cal_distance(cls, x1, y1, x2, y2):
        return math.sqrt(cls.cal_distance_square(x1, y1, x2, y2))
