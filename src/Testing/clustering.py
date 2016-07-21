import nltk
import cloudant
import requests
import csv
import sys
import extract_keywords
from cloudant.query import Query
SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'                                                                                                    #Replace with your server URL
DATABASE = 'amazon_data'                                                                                                #Replace with the name of the database
USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'                                                                                               #Replace with the username from your credentials for the NLC
PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'
DESIGN = 'names'                                                                                                        #replace with the name of the design document that contains the view. This should be of the form '_design/XXXX'
VIEW =          'asinview'                                                                                              #Replace with the view from your database to poll, this should take the form of view_file/view and should return the text to classify as the value field and what you would like to call it as the key
DESTINATION = 'out1.csv'                                                                                                                        #Replace with correct name for output file (NOTE must be *.csv)


from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import random
from scipy import spatial
import numpy as np

server = cloudant.client.Cloudant(USERNAME,PASSWORD,url=SERVER)
server.connect()
db = server[DATABASE]
query = Query(db, selector={'asin':'B00BCGRZ04'},fields=["_id"])


client_username='fc5dda33-3709-459b-8857-92b93630db31-bluemix'
client_password='a15d0990d5ebfb2aedd5a61dacdbdb132b6e2266f74a7f46cadfadbc6b982b06'
client_database='testdb_final'
#client_server='https://fc5dda33-3709-459b-8857-92b93630db31-bluemix.cloudant.com'
#client_db=cloudant.client.Cloudant(client_username,client_password,account=client_username)
#client_db.connect()

temp_client = cloudant.client.Cloudant("fc5dda33-3709-459b-8857-92b93630db31-bluemix","a15d0990d5ebfb2aedd5a61dacdbdb132b6e2266f74a7f46cadfadbc6b982b06",account="fc5dda33-3709-459b-8857-92b93630db31-bluemix")
temp_client.connect()

db_2=temp_client[client_database]
rev_id=[]
for data in query.result:
	rev_id.append(data['_id'])

print rev_id
rev_id=["0000927a59e02ee3d09b12e0e202bba5","0000927a59e02ee3d09b12e0e202dd2b","0000927a59e02ee3d09b12e0e202f3f2","0000927a59e02ee3d09b12e0e2056019"]
temp={}
keys=[]
for rev in rev_id:	
	query_id=Query(db_2, selector={'review_id':rev})
	res=query_id.result[0][0]
	#rev=query_id.result[0]
	#print "\n"
	print res
	text=res['review']
	for obj in text:
		if 'Feature' in obj:
			feature=obj['Feature']
			for data in feature:
				temp={}
				temp['word']=data['name']
				if 'sentiment' in data:
					temp['sentiment']=data['sentiment']
				else:
					temp['sentiment']=['Neutral']
				temp['rev_id']=res['review_id']
				temp['sentence_id']=obj['seqno']
				print temp
				keys.append(temp)
print keys

sentences = word2vec.Text8Corpus('text8')
modelname='sample_model'

def train(sentences,modelname):
        model = word2vec.Word2Vec(sentences, size=200)
        model.save(modelname)
        model.save_word2vec_format(modelname+'.bin', binary=True)

#train(sentences,modelname)

model = word2vec.Word2Vec.load_word2vec_format(modelname+'.bin', binary=True)
print model.similarity('sound','cans')
print "gaming"

def generate_vectors(features):
        #fp=open('unique_sample_TV.txt')    ##file with input keywords
        #fw=open('obtained_keywords_TV_unique.txt','w')   ##file with output keywords
        vecs=[]
        #keywords=[]

        for line in features:
                print line
                words=line['word'].split()
                no=len(words)
                vec=[]
                flag=0
                for word in words:
                        if word in model:
                                if len(vec)>1:
                                        vec=vec+model[word]
                                else:
                                        vec=model[word]
                        else:
                                flag=1
                                break
                if flag==0:
                        #keywords.append(line)
                        if len(vec)>0:
                                #vec=vec
                                vecs.append(vec)

        return vecs
        #print keywords
        #for keyword in keywords:
        #        fw.write(keyword)
        #np.save('keywords_vecs_TV_unique.npy',vecs)  ###vectors
        #np.save('keywords_TV_unique.npy',keywords)   ###keywords

vecs=generate_vectors(keys)
#features and stuff- array of json	
#cluster features
##sentiment aggregation
##final json

def cluster_try(vecs):
        clusterVec={}
        clusterIdx={}
        no_of_clusters=1
        id=0
        clusterIdx[0]=[0]
        #clusterIdx[0].append([0])
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

clusters=cluster_try(vecs)

def create_json(clusters):
	print clusters
	for i in clusters:
		keyword_count=0
		pos=0
		neg=0
		neutral=0
		unique_words={}
		clusterinfo={}
		for key in clusters[i]:
			#clusterinfo={}			
			keyword= keys[key]['word']
			if keyword in unique_words:
				unique_words[keyword]['count']+=1
				unique_words[keyword]['review_id'].append(keys[key]['rev_id'])
				unique_words[keyword]['sentence_id'].append(keys[key]['sentence_id'])
			else:
				unique_words[keyword]={}
				unique_words[keyword]['count']=1
				unique_words[keyword]['review_id']=[keys[key]['rev_id']]
				unique_words[keyword]['sentence_id']=[keys[key]['sentence_id']]
			keyword_count+=1
			print unique_words
			list_keywords=[]
			for feature in unique_words:
				data={}
				data['keyword']=feature
				data['sentence_id']=unique_words[feature]['sentence_id']
				data['review_id']=unique_words[feature]['review_id']
				list_keywords.append(data)
			#clusterinfo['keywords']=list_keywords
			if keys[key]['sentiment'][0]=='positive':
					pos+=1
			if keys[key]['sentiment'][0]=='Neutral':
					neutral+=1
			if keys[key]['sentiment'][0]=='negative':
					neg+=1
		clusterinfo['keywords']=list_keywords
		clusterinfo['sentiments']={}
		clusterinfo['sentiments']['positive']=pos
		clusterinfo['sentiments']['negative']=neg
		clusterinfo['sentiments']['neutral']=neutral
		clusterinfo['keyword_count']=keyword_count
		for w in sorted(unique_words, key=unique_words.get, reverse=True):
			name=w
			clusterinfo['feature']=name
			print w
		print clusterinfo
	

print create_json(clusters)
			
			
		
