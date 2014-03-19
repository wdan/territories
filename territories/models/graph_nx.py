# -*- coding: utf-8 -*-

import json
from random import randint

import networkx as nx
from networkx.readwrite import json_graph
from graph import AbstractGraph
from graph_generator import GraphGenerator
from data_politicsuk import PoliticsUK as DataSet
from force_directed import ForceDirectedLayout
from mds import MDSLayout
from util import translate, jsonize


class NXGraph(AbstractGraph):

    ADJUST_NUMBER = 0
    MAX_SIZE = 1000

    def __init__(self, g_type="all", width=1000, height=1000):
        self.width = width
        self.height = height
        self.nx_g = nx.Graph()
        if g_type == "r_cluster":
            self.init_r_cluster()
        elif g_type == "d_cluster":
            self.init_d_cluster()
        else:
            self.init_all()

    @property
    def size(self):
        return len(self.nx_g.nodes())

    def init_all(self):
        self.nx_g.clear()
        self.import_nodes()
        self.import_edges()
        self.import_communities()

    #def reduce_graph(self, rate, c_l_d, c_p_d):
    def reduce_graph(self, c_l_d):
        self.cal_degree(c_l_d)
        #(inner_edges_dict, outer_edges_dict) = self.adjust_edges()
        #(inner_nodes_dict, outer_nodes_dict) = self.adjust_nodes()
        #self.cal_outer_positions(rate, outer_nodes_dict, outer_edges_dict, c_l_d)
        #self.cal_inner_positions(inner_nodes_dict, inner_edges_dict, c_p_d)

    def init_d_cluster(self):
        self.nx_g.clear()
        self.import_cluster_nodes()
        self.import_cluster_edges()

    def init_r_cluster(self):
        generator = GraphGenerator(12, 20, edge_pr_btw_com=0.02, low=0.2, high=2)
        self.nx_g = generator.get_nx()
        #g = generator.get_ig()
        #cv = generator.community_detection(g)
        #original_graph = generator.get_nx()
        #clustered_graph = generator.convert2nx(cv)

    def cal_mds_positions(self, src=None, tgt=None):
        (matrix, m) = self.cal_edge_weight_matrix(src, tgt)
        p = MDSLayout.cal_mds(matrix, m)
        x_min = min(map(lambda e: e[0], p))
        x_max = max(map(lambda e: e[0], p))
        y_min = min(map(lambda e: e[1], p))
        y_max = max(map(lambda e: e[1], p))
        for i, e in enumerate(self.nx_g.nodes()):
            self.nx_g.node[e]["x"] = translate(p[i][0], x_min, x_max,
                                               0, self.width)
            self.nx_g.node[e]["y"] = translate(p[i][1], y_min, y_max,
                                               0, self.height)

    def cal_edge_weight_matrix(self, src=None, tgt=None):
        n = self.size
        m = 0
        matrix = [[0 for x in xrange(n)] for x in xrange(n)]
        node_dict = {}
        max_weight = 0
        for i, e in enumerate(self.nx_g.nodes()):
            node_dict[e] = i
        for e in self.nx_g.edges():
            index0 = node_dict[e[0]]
            index1 = node_dict[e[1]]
            weight = self.nx_g.edge[e[0]][e[1]]["weight"]
            if weight > max_weight:
                max_weight = weight
            matrix[index0][index1] = int(weight)
            matrix[index1][index0] = int(weight)
            if m < weight:
                m = weight
        if src != -1 and src != None:
            index0 = node_dict[src]
            index1 = node_dict[tgt]
            matrix[index0][index1] = max_weight * 1.5
            matrix[index1][index0] = max_weight * 1.5
        for i in xrange(n):
            matrix[i][i] = int(m * 1.5)
        return (matrix, int(m * 1.5))

    def cal_inner_positions(self, inner_nodes_dict, inner_edges_dict, constraints_dict):
        p = ForceDirectedLayout.cal_rd_layout(inner_nodes_dict, inner_edges_dict, constraints_dict)
        for i, e in enumerate(inner_nodes_dict.keys()):
            if e in p:
                self.nx_g.node[e]["x"] = p[e]["x"]
                self.nx_g.node[e]["y"] = p[e]["y"]

    def cal_outer_positions(self, rate, outer_nodes_dict, outer_edges_dict, constraints_dict):
        p = ForceDirectedLayout.cal_fd_layout(outer_nodes_dict, outer_edges_dict,
                                              self.width, self.height, constraints_dict)
        for i, e in enumerate(outer_nodes_dict.keys()):
            if e in p:
                p[e]["out_degree"] = self.nx_g.node[e]["out_degree"]
                self.nx_g.node[e]["x"] = p[e]["x"]
                self.nx_g.node[e]["y"] = p[e]["y"]
        p = sorted(p.items(), key=lambda (k, v): v["out_degree"])
        p = dict(p[-int(len(p) * rate):])
        for i, e in enumerate(outer_nodes_dict.keys()):
            if e in p:
                self.nx_g.node[e]["visible"] = 1
            else:
                self.nx_g.node[e]["visible"] = 0

        for i, e in enumerate(outer_edges_dict.keys()):
            cluster1 = self.nx_g.node[e[0]]["cluster"]
            cluster2 = self.nx_g.node[e[1]]["cluster"]
            if ((cluster1, cluster2) in constraints_dict) and e[0] in p and e[1] in p:
                self.nx_g.edge[e[0]][e[1]]["visible"] = 1
            else:
                self.nx_g.edge[e[0]][e[1]]["visible"] = 0

    def cal_cluster_voronoi_positions(self, src = None, tgt = None):
        self.cal_mds_positions(src, tgt)
        from py4j.java_gateway import JavaGateway
        gateway = JavaGateway(auto_convert=True)
        java_app = gateway.entry_point
        x = []
        y = []
        w = []
        cluster = []
        for n in self.nx_g.nodes():
            if "x" in self.nx_g.node[n]:
                t_x = float(self.nx_g.node[n]["x"])
            else:
                t_x = float(randint(0, self.width))
            if "y" in self.nx_g.node[n]:
                t_y = float(self.nx_g.node[n]["y"])
            else:
                t_y = float(randint(0, self.height))
            if "size" in self.nx_g.node[n]:
                t_w = float(self.nx_g.node[n]["size"])
            else:
                t_w = float(randint(0, self.MAX_SIZE))
            x.append(t_x)
            y.append(t_y)
            w.append(t_w)
            cluster.append(n)
        res = java_app.calVoronoiTreemap(x, y, w, cluster,self.width, self.height)
        return res

    def import_cluster_nodes(self):
        res = DataSet.import_cluster_nodes()
        for i, e in enumerate(res.keys()):
            self.nx_g.add_node(e, size=res[e])

    def import_cluster_edges(self):
        res = DataSet.import_cluster_edges()
        for key in res.keys():
            attributes = res[key]
            self.nx_g.add_edge(key[0], key[1])
            for attr in attributes.keys():
                self.nx_g.edge[key[0]][key[1]][attr] = attributes[attr]

    def import_nodes(self):
        res = DataSet.import_nodes()
        for key in res.keys():
            self.nx_g.add_node(key)
            attributes = res[key]
            for attr in attributes.keys():
                self.nx_g.node[key][attr] = attributes[attr]

    def import_edges(self):
        res = DataSet.import_edges()
        for e in res:
            self.nx_g.add_edge(e[0], e[1])

    def import_communities(self):
        (n, res) = DataSet.import_communities()
        self.nx_g.graph["community-num"] = n
        for key in res.keys():
            self.nx_g.node[key]["cluster"] = res[key]

    @classmethod
    def mark_community(cls, g):
        clustered_graph = nx.Graph()
        community_dict = {}
        community_size_dict = {}
        node2community_dict = {}
        cnt = 0
        for n in g.nodes():
            community = g.node[n]["class"]
            if type(community) is dict:
                c_list = sorted(community.items(), key=lambda (k, v): v)
                community = c_list[-1][0]
            if community not in community_dict:
                community_dict[community] = cnt
                community_size_dict[community] = 0
                cnt += 1
            community_size_dict[community] += 1
            community_id = community_dict[community]
            node2community_dict[n] = community_id
            g.node[n]["cluster"] = community_id

        for key in community_dict.keys():
            cluster_id = community_dict[key]
            clustered_graph.add_node(cluster_id)
            clustered_graph.node[cluster_id]["size"] = community_size_dict[key]
            clustered_graph.node[cluster_id]["cluster-name"] = key

        edges_dict = {}
        inner_edges_dict = {}
        outer_edges_dict = {}
        for e in g.edges():
            src_id = node2community_dict[e[0]]
            tgt_id = node2community_dict[e[1]]
            if src_id == tgt_id:
                if src_id not in inner_edges_dict:
                    inner_edges_dict[src_id] = 0
                inner_edges_dict[src_id] += 1
                continue
            if src_id > tgt_id:
                src_id, tgt_id = tgt_id, src_id
            if (src_id, tgt_id) not in edges_dict:
                edges_dict[(src_id, tgt_id)] = 0
            if src_id not in outer_edges_dict:
                outer_edges_dict[src_id] = 0
            if tgt_id not in outer_edges_dict:
                outer_edges_dict[tgt_id] = 0
            outer_edges_dict[src_id] += 1
            outer_edges_dict[tgt_id] += 1
            edges_dict[(src_id, tgt_id)] += 1

        for n in clustered_graph.nodes():
            inner_edges_num = inner_edges_dict[n]
            outer_edges_num = outer_edges_dict[n]
            quality = outer_edges_num * 1.0 / (2 * inner_edges_num + outer_edges_num)
            clustered_graph.node[n]["quality"] = quality

        for (k, v) in edges_dict.items():
            clustered_graph.add_edge(k[0], k[1])
            clustered_graph.edge[k[0]][k[1]]["weight"] = v
        return clustered_graph

    def cal_degree(self, constraints_dict):
        edges = self.nx_g.edges()
        node_dict = {}
        for e in edges:
            node0 = self.nx_g.node[e[0]]
            node1 = self.nx_g.node[e[1]]
            if e[0] not in node_dict:
                node_dict[e[0]] = {}
                node_dict[e[0]]["in_degree"] = 0
                node_dict[e[0]]["out_degree"] = 0
                node_dict[e[0]]["tgt_clusters"] = {}
            if e[1] not in node_dict:
                node_dict[e[1]] = {}
                node_dict[e[1]]["in_degree"] = 0
                node_dict[e[1]]["out_degree"] = 0
                node_dict[e[1]]["tgt_clusters"] = {}
            if node0["cluster"] == node1["cluster"]:
                node_dict[e[0]]["in_degree"] += 1
                node_dict[e[1]]["in_degree"] += 1
            else:
                node_dict[e[0]]["out_degree"] += 1
                node_dict[e[1]]["out_degree"] += 1
                if node0["cluster"] not in node_dict[e[1]]["tgt_clusters"]:
                    node_dict[e[1]]["tgt_clusters"][node0["cluster"]] = 0
                node_dict[e[1]]["tgt_clusters"][node0["cluster"]] += 1
                if node1["cluster"] not in node_dict[e[0]]["tgt_clusters"]:
                    node_dict[e[0]]["tgt_clusters"][node1["cluster"]] = 0
                node_dict[e[0]]["tgt_clusters"][node1["cluster"]] += 1
        for n in self.nx_g.nodes():
            if n not in node_dict:
                self.nx_g.remove_node(n)
                continue
            if node_dict[n]["in_degree"] + node_dict[n]["out_degree"] == 0:
                self.nx_g.remove_node(n)
                continue
            self.nx_g.node[n]["visible"] = 1
            self.nx_g.node[n]["external"] = 0
            self.nx_g.node[n]["in_degree"] = node_dict[n]["in_degree"]
            self.nx_g.node[n]["out_degree"] = node_dict[n]["out_degree"]
            src_cluster = self.nx_g.node[n]["cluster"]
            if self.nx_g.node[n]["out_degree"] > 0:
                self.nx_g.node[n]["external"] = 1
                max_tgt = 0
                index = -1
                for key in node_dict[n]["tgt_clusters"].keys():
                    if max_tgt < node_dict[n]["tgt_clusters"][key] and (src_cluster, key) in constraints_dict:
                        max_tgt = node_dict[n]["tgt_clusters"][key]
                        index = key
                if index == -1:
                    self.nx_g.node[n]["out_degree"] = 0
                    self.nx_g.node[n]["external"] = 0
                else:
                    self.nx_g.node[n]["out_degree"] = max_tgt
                    self.nx_g.node[n]["tgt_cluster"] = index

    def adjust_nodes(self):
        outer_nodes_dict = {}
        inner_nodes_dict = {}
        for e in self.nx_g.nodes():
            if self.nx_g.node[e]["external"] == 1 and self.nx_g.node[e]["out_degree"] > self.ADJUST_NUMBER:
                outer_nodes_dict[e] = self.nx_g.node[e]
            elif self.nx_g.node[e]["external"] == 0:
                inner_nodes_dict[e] = self.nx_g.node[e]
        sorted_o_f_n = sorted(outer_nodes_dict.items(), key=lambda (k, v): v["out_degree"])
        for e in sorted_o_f_n:
            self.nx_g.node[e[0]]["visible"] = 0
        sorted_o_f_n = dict(sorted_o_f_n)
        sorted_i_f_n = inner_nodes_dict
        return (sorted_i_f_n, sorted_o_f_n)

    def adjust_edges(self):
        inner_edges_dict = {}
        outer_edges_dict = {}
        for e in self.nx_g.edges():
            num0 = self.nx_g.node[e[0]]["out_degree"]
            num1 = self.nx_g.node[e[1]]["out_degree"]
            src_cluster0 = self.nx_g.node[e[0]]["cluster"]
            src_cluster1 = self.nx_g.node[e[1]]["cluster"]
            if num0 > 0 and num1 > 0:
                if num0 > self.ADJUST_NUMBER and num1 > self.ADJUST_NUMBER:
                    tgt_cluster0 = self.nx_g.node[e[0]]["tgt_cluster"]
                    tgt_cluster1 = self.nx_g.node[e[1]]["tgt_cluster"]
                    #if src_cluster0 == tgt_cluster1 and src_cluster1 == tgt_cluster0:
                    if src_cluster0 != src_cluster1:
                        self.nx_g.edge[e[0]][e[1]]["visible"] = 1
                        outer_edges_dict[(e[0], e[1])] = self.nx_g.edge[e[0]][e[1]]
                    else:
                        if src_cluster0 != src_cluster1:
                            self.nx_g.node[e[0]]["out_degree"] -= 1
                            if self.nx_g.node[e[0]]["out_degree"] == 0:
                                self.nx_g.node[e[0]]["external"] = 0
                            self.nx_g.node[e[1]]["out_degree"] -= 1
                            if self.nx_g.node[e[1]]["out_degree"] == 0:
                                self.nx_g.node[e[1]]["external"] = 0
                        self.nx_g.edge[e[0]][e[1]]["visible"] = 0
            elif num0 > 0 or num1 > 0:
                if src_cluster0 == src_cluster1:
                    self.nx_g.edge[e[0]][e[1]]["visible"] = 1
                else:
                    self.nx_g.edge[e[0]][e[1]]["visible"] = 0
            else:
                if src_cluster0 == src_cluster1:
                    self.nx_g.edge[e[0]][e[1]]["visible"] = 1
                    inner_edges_dict[(e[0], e[1])] = self.nx_g.edge[e[0]][e[1]]
                else:
                    self.nx_g.edge[e[0]][e[1]]["visible"] = 0
        return (inner_edges_dict, outer_edges_dict)

    @classmethod
    def to_json(cls, g):
        return json_graph.dumps(g)

    @jsonize
    def get_detailed_info(self):
        g = self.nx_g
        node_dict = {}
        for e in g.edges:
            src_cluster = g.node[e[0]]["cluster"]
            tgt_cluster = g.node[e[1]]["cluster"]
            if e[0] not in node_dict:
                node_dict[e[0]] = {}
            if e[1] not in node_dict:
                node_dict[e[1]] = {}
            if tgt_cluster not in node_dict[e[0]]:
                node_dict[e[0]][tgt_cluster] = 0
            if src_cluster not in node_dict[e[1]]:
                node_dict[e[1]][src_cluster] = 0
            node_dict[e[0]][tgt_cluster] += 1
            node_dict[e[1]][src_cluster] += 1
        cluster_dict = {}
        for key in node_dict.keys():
            src_cluster = g.node[key]["cluster"]
            tgt_clusters = node_dict[key]
            for tgt_cluster in tgt_clusters:
                if (src_cluster, tgt_cluster) not in cluster_dict:
                    cluster_dict[(src_cluster, tgt_cluster)] = {}
                    cluster_dict[(src_cluster, tgt_cluster)]["src_cluster"] = src_cluster
                    cluster_dict[(src_cluster, tgt_cluster)]["tgt_cluster"] = tgt_cluster
                    cluster_dict[(src_cluster, tgt_cluster)]["points"] = []
            cluster_dict[(src_cluster, tgt_cluster)]["points"].append(key)
        res = []
        for key in node_dict.keys():
            res.append(node_dict[key])
        return res

    @jsonize
    def get_constraints_nodes(self, constraints):
        g = self.nx_g
        cluster_dic = {}
        mid_dic = {}
        for n in g.nodes():
            if g.node[n]["external"] > 0:
                src_c = g.node[n]["cluster"]
                tgt_c = g.node[n]["tgt_cluster"]
                if (src_c, tgt_c) not in cluster_dic:
                    cluster_dic[(src_c, tgt_c)] = []
                cluster_dic[(src_c, tgt_c)].append(n)
        for c in constraints.keys():
            cluster = c[0]
            constraint = constraints[c]
            if cluster not in mid_dic:
                mid_dic[cluster] = {}
                mid_dic[cluster]["x"] = constraint.mid_x
                mid_dic[cluster]["y"] = constraint.mid_y
        res_dic = []
        for c in constraints.keys():
            src_c = c[0]
            tgt_c = c[1]
            constraint = constraints[c]
            if (src_c, tgt_c) in cluster_dic:
                res_item = {}
                res_item["src_cluster"] = src_c
                res_item["tgt_cluster"] = tgt_c
                res_item["x1"] = constraint.x1
                res_item["y1"] = constraint.y1
                res_item["x2"] = constraint.x2
                res_item["y2"] = constraint.y2
                res_item["src_cluster_x"] = mid_dic[src_c]["x"]
                res_item["src_cluster_y"] = mid_dic[src_c]["y"]
                res_item["tgt_cluster_x"] = mid_dic[tgt_c]["x"]
                res_item["tgt_cluster_y"] = mid_dic[tgt_c]["y"]
                res_item["points"] = []
                for n in cluster_dic[src_c, tgt_c]:
                    point_item = {}
                    point_item["in_degree"] = g.node[n]["in_degree"]
                    point_item["out_degree"] = g.node[n]["out_degree"]
                    point_item["cluster"] = g.node[n]["cluster"]
                    if "label" in g.node[n]:
                        point_item["label"] = g.node[n]["label"]
                    res_item["points"].append(point_item)
                res_dic.append(res_item)
        return res_dic
