import nltk
import requests
import csv
import sys
import extract_keywords
from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import random
from scipy import spatial
import numpy as np

temp={}
keys=[]

def create_json(clusters):
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
		return clusterinfo

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
                                #break
                if flag==0:
                        clusterIdx[j+1]=[i]
                        clusterVec[j+1]=vecs[i]
                        no_of_clusters+=1
                else:
                        clusterIdx[index].append(i)
                        clusterVec[index]+=vecs[i]
        return clusterIdx


def generate_vectors(features):
        #fp=open('unique_sample_TV.txt')    ##file with input keywords
        #fw=open('obtained_keywords_TV_unique.txt','w')   ##file with output keywords
        vecs=[]
        #keywords=[]

        for line in features:
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


def train(sentences,modelname):
        model = word2vec.Word2Vec(sentences, size=200)
        model.save(modelname)
        model.save_word2vec_format(modelname+'.bin', binary=True)


def cluster(review):
	text=review['review']
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
				keys.append(temp)


	sentences = word2vec.Text8Corpus('text8')
	modelname='sample_model'
	train(sentences,modelname)

	model = word2vec.Word2Vec.load_word2vec_format(modelname+'.bin', binary=True)
	vecs=generate_vectors(keys)
	clusters=cluster_try(vecs)
	out = create_json(clusters)

	final = {}
	final['features'] = out
	final['type'] = ['clustered']
	return final
