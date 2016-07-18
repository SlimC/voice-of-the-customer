import numpy as np
import scipy.spatial.distance as distance

def crp(vecs):
    clusterVec = [0]         # tracks sum of vectors in a cluster
    clusterIdx = [0]         # array of index arrays. e.g. [[1, 3, 5], [2, 4, 6]]
    ncluster = 0
    # probablity to create a new table if new customer
    # is not strongly "similar" to any existing table
    pnew = 1.0/ (1 + ncluster)
    N = len(vecs)
    rands = np.random.rand(N)         # N rand variables sampled from U(0, 1)

    for i in range(N):
        maxSim = - np.inf
        maxIdx = 0
        v = vecs[i]
        for j in range(ncluster):
            sim = distance.cosine(v, clusterVec[j])
            if sim < maxSim:
                maxIdx = j
                maxSim = sim
            if maxSim < pnew:
                if np.numpy.random.rand(i) < pnew:
                    clusterVec[ncluster] = v
                    clusterIdx[ncluster] = [i]
                    ncluster += 1
                    pnew = 1.0 / (1 + ncluster)
                continue
        clusterVec[maxIdx] = clusterVec[maxIdx] + v
        clusterIdx[maxIdx].append(i)

    return clusterIdx

def word_cluster():
    keywords = np.load('keywords.npy')
    vectors = np.load('keywords_vecs.npy')

    cluster_vecs = crp(vectors)

    for cluster in cluster_vecs:
        for word in cluster:
            cluster_vecs[cluster][word] = keywords[word]
    return clusters
