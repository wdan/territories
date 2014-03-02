# -*- coding: utf-8 -*-


class PoliticsUK(object):

    @classmethod
    def import_cluster_nodes(cls):
        communities_file = open("territories/data/politicsuk.communities", "r")
        communities_cnt = {}
        cls.item_to_communities = {}
        for i, row in enumerate(communities_file):
            row_entries = row.split(":")
            nodes_id_list = row_entries[1].split(",")
            for e in nodes_id_list:
                cls.item_to_communities[int(e)] = i
                if i in communities_cnt:
                    communities_cnt[i] += 1
                else:
                    communities_cnt[i] = 0
        return communities_cnt

    @classmethod
    def import_cluster_edges(cls):
        dics = {}
        res = {}
        matrix = [[0 for x in xrange(5)] for x in xrange(5)]
        for i in xrange(5):
            for j in xrange(5):
                matrix[i][j] = 0
        edges_file = open("territories/data/politicsuk-follows.mtx", "r")
        for i, row in enumerate(edges_file):
            if i == 0:
                continue
            row_entries = row.split()
            if (int(row_entries[1]), int(row_entries[0])) in dics:
                community1 = cls.item_to_communities[int(row_entries[0])]
                community2 = cls.item_to_communities[int(row_entries[1])]
                matrix[community1][community2] += 1
            else:
                dics[(int(row_entries[0]), int(row_entries[1]))] = 1

        for i in xrange(5):
            for j in xrange(i+1, 5):
                if (matrix[i][j] + matrix[j][i] > 0):
                    res[(i, j)] = {}
                    res[(i, j)]["weight"] = matrix[i][j] + matrix[j][i]
        return res

    @classmethod
    def import_nodes(cls):
        #nodes_file = open("territories/data/politicsuk.ids", "r")
        nodes_file = open("../data/politicsuk.ids", "r")
        res = {}
        for row in nodes_file:
            res[int(row)] = {}
            res[int(row)]["cluster"] = 0
        return res

    @classmethod
    def import_edges(cls):
        #edges_file = open("territories/data/politicsuk-retweets.mtx", "r")
        edges_file = open("../data/politicsuk-retweets.mtx", "r")
        dics = {}
        res = []
        for i, row in enumerate(edges_file):
            if i == 0:
                continue
            row_entries = row.split()
            if (int(row_entries[1]), int(row_entries[0])) in dics:
                res.append((int(row_entries[0]), int(row_entries[1])))
            else:
                dics[(int(row_entries[0]), int(row_entries[1]))] = 1
        return res

    @classmethod
    def import_communities(cls):
        #communities_file = open("territories/data/politicsuk.communities", "r")
        communities_file = open("../data/politicsuk.communities", "r")
        res = {}
        for i, row in enumerate(communities_file):
            row_entries = row.split(":")
            nodes_id_list = row_entries[1].split(",")
            for e in nodes_id_list:
                res[int(e)] = i + 1
        return res
