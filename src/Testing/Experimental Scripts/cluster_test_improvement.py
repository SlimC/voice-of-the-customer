def crp(vecs):
    clusterVec = []         # tracks sum of vectors in a cluster
    clusterVec.append([0,0,0])
    clusterIdx = []         # array of index arrays. e.g. [[1, 3, 5], [2, 4, 6]]
    clusterIdx.append([])
    ncluster = 0
    # probablity to create a new table if new customer
    # is not strongly "similar" to any existing table
    pnew = 1.0/ (1 + ncluster)
    N = len(vecs)
    rands = np.random.rand(N)         # N rand variables sampled from U(0, 1)

    for i in range(N):
        maxSim = -1000000000000000
        maxIdx = 0
        v = vecs[i]
        for j in range(ncluster):
            sim = spatial.distance.cosine(v, clusterVec[j])
            print sim
            if sim < maxSim:
                maxIdx = j
                maxSim = sim
            if maxSim < pnew:
                if rands(i) < pnew:
                    clusterVec[ncluster] = v
                    clusterIdx[ncluster] = [i]
                    ncluster += 1
                    pnew = 1.0 / (1 + ncluster)
                continue
        clusterVec[maxIdx] = clusterVec[maxIdx] + v
        clusterIdx[maxIdx].append(i)

    return clusterIdx
import numpy as np
key_vecs=np.load('keywords_vecs.npy')
#print key_vecs[-1]
words=np.load('keywords.npy')
fw=open('clusters_improved.txt','w')

def cluster_try(vecs):
	clusterVec={}
	clusterIdx={}
	no_of_clusters=1
	id=0
	clusterIdx[0]=[]
	clusterIdx[0].append([0])
	clusterVec[0]=vecs[0]
	max_sim=0.5
	index=0
	for i in range(1,len(vecs)):
		flag=0
		max_sim=0.5
		for j in range(no_of_clusters):
			sim=np.dot(vecs[i],clusterVec[j])/(np.linalg.norm(clusterVec[j])* np.linalg.norm(vecs[i]))
			#sim=cosine(vecs[i],clusterVec[j])
			if sim>max_sim :
				#clusterIdx[j].append(i)
				#clusterVec[j]+=vecs[i]	
				flag=1
				max_sim=sim
				index=j
				print "\n index"
				print index
				#break
		if flag==0:
			clusterIdx[j+1]=[i]
			clusterVec[j+1]=vecs[i]
			no_of_clusters+=1
		else:
			clusterIdx[index].append(i)
			clusterVec[index]+=vecs[i]
	return clusterIdx
	
clusterIdx=cluster_try(key_vecs)
print "cluster\n"				
for i in clusterIdx:
	fw.write('__________________')
	fw.write('cluster'+str(i)+'\n')
	print clusterIdx[i]
	for j in clusterIdx[i]:
		print words[j]
		fw.write(words[j])
print crp([[1,2,3],[4,5,6]])
