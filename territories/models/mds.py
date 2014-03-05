__author__ = 'wenbin'

import numpy as np
from sklearn import manifold


class MDSLayout(object):

    @classmethod
    def cal_mds(cls, data, veryLarge):
        n = len(data)
        similarities = []
        for i in xrange(n):
            list = data[i]
            tmp = [(veryLarge - j) for j in list]
            similarities += tmp
            #print similarities
        similarities = np.array(similarities)
        similarities = np.ndarray((n, n), buffer=similarities, dtype=int)
        #print similarities
        mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                           dissimilarity="precomputed", n_jobs=1)
        pos = mds.fit(similarities).embedding_
        #print pos
        return pos

if __name__ == "__main__":
    veryLarge = int(442.5)
    data = [[veryLarge, 295, 74, 3, 6], [295, veryLarge, 82, 11, 13],
            [74, 82, veryLarge, 0, 4], [3, 11, 0, veryLarge, 5],
            [6, 13, 4, 5, veryLarge]]
    print MDSLayout.cal_mds(data, veryLarge)
