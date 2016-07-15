from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def train(sentences,modelname):
	model = word2vec.Word2Vec(sentences, size=200)
	model.save(modelname)
	model.save_word2vec_format(modelname+'.bin', binary=True)


#model = word2vec.Word2Vec.load_word2vec_format(modelname+'.bin', binary=True)
#print model.most_similar(['girl', 'father'], ['boy'], topn=3)
#print model['mid']
import random
from scipy import spatial
import numpy as np

def generate_vectors():
	fp=open('sample_test.txt')    ##file with input keywords
	fw=open('obtained_keywords.txt','w')   ##file with output keywords
	vecs=[]
	keywords=[]

	for line in fp:
		print line
		words=line.split()
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
			keywords.append(line)
			if len(vec)>0:
				#vec=vec	
				vecs.append(vec)
			
	print vecs	
	print keywords
	for keyword in keywords:
		fw.write(keyword)
	np.save('keywords_vecs.npy',vecs)  ###vectors
	np.save('keywords.npy',keywords)   ###keywords

sentences = word2vec.Text8Corpus('text8')
modelname='sample_model'
model = word2vec.Word2Vec.load_word2vec_format(modelname+'.bin', binary=True)
#train first time
#train(sentences,modelname)
generate_vectors()

