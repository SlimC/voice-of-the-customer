import numpy as np
import scipy.spatial.distance as distance

def crp(vecs):
    clusterVec = [vecs[0]]         # tracks sum of vectors in a cluster
    clusterIdx = [[0]]         # array of index arrays. e.g. [[1, 3, 5], [2, 4, 6]]
    ncluster = 1
    print clusterVec
    # # probablity to create a new table if new customer
    # # is not strongly "similar" to any existing table
    pnew = 1.0/ (1 + ncluster)
    N = len(vecs)
    rand = np.random.rand         #rand variables sampled from U(0, 1)
    for i in range(1,N):
        print i
        maxSim = -np.inf
        maxIdx = None
        v = vecs[i]
        for j in range(ncluster):
            print v.shape
            print clusterVec[j].shape
            sim = distance.cosine(v, clusterVec[j])
            if sim > pnew:
                if sim > maxSim:
                    maxIdx = j
                    sim = maxSim
                    print "maxId: " + str(j)
        print maxIdx
        if maxIdx is not None:
            clusterVec[maxIdx] += v
            clusterIdx[maxIdx].append(i)
            print "appended: ids = " + str(clusterIdx)
        else:
            for j in range(ncluster):
                if rand() < pnew:
                    clusterVec.append(v)
                    clusterIdx.append([i])
                    ncluster += 1
                    pnew = 1.0/(1+ncluster)
                    print clusterVec
                    print clusterIdx
                    print ncluster
                    print pnew
                    break
                else:
                    clusterVec[j] += v
                    clusterIdx[j].append(i)
                    print clusterVec
                    print clusterIdx
                    break
    return clusterIdx

def word_cluster():
    keywords = np.load('keywords.npy')
    vectors = np.load('keywords_vecs.npy')
    cluster_vecs = crp(vectors)
    print type(cluster_vecs)
    for i in range(len(cluster_vecs)):
        for j in range(len(cluster_vecs[i])):
            cluster_vecs[i][j] = keywords[cluster_vecs[i][j]]
    return cluster_vecs
