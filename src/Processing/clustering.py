import cloudant
from cloudant.query import Query
from gensim.models import word2vec
import logging
import numpy as np
import re
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def train(sentences, modelname):
        model = word2vec.Word2Vec(sentences, size=200)
        model.save(modelname)
        model.save_word2vec_format(modelname+'.bin', binary=True)


def generate_vectors(features, model):
    vecs = []
    mapping = []
    count = 0
    for line in features:
        words = line['word'].split()
        vec = []
        flag = 0
        for word in words:
            word = str(word)
            word = re.escape(word)
            word = re.sub(r'\\', '', word)
            if word in model:
                if len(vec) > 1:
                    vec = vec+model[word]
                else:
                    vec = model[word]
            else:
                flag = 1
                break
        if flag == 0:
            if len(vec) > 0:
                vecs.append(vec)
                mapping.append(count)
        count += 1

    return [vecs, mapping]


def cluster_try(vecs):
        clusterVec = {}
        clusterIdx = {}
        no_of_clusters = 1
        clusterIdx[0] = [0]
        clusterVec[0] = vecs[0]
        max_sim = 0.5
        index = 0
        for i in range(1, len(vecs)):
                flag = 0
                max_sim = 0.5
                for j in range(no_of_clusters):
                        sim = np.dot(vecs[i], clusterVec[j])/(np.linalg.norm(clusterVec[j]) * np.linalg.norm(vecs[i]))
                        if sim > max_sim:
                                flag = 1
                                max_sim = sim
                                index = j
                if flag == 0:
                        clusterIdx[j+1] = [i]
                        clusterVec[j+1] = vecs[i]
                        no_of_clusters += 1
                else:
                        clusterIdx[index].append(i)
                        clusterVec[index] += vecs[i]
        return clusterIdx


def create_json(clusters, cluster_data, mapping, keys, helpful, local_dump):
    for i in clusters:
        keyword_count = 0
        pos = 0
        neg = 0
        neutral = 0
        unique_words = {}
        clusterinfo = {}
        for key in clusters[i]:
            index = mapping[key]
            keyword = keys[index]['word']
            if keyword in unique_words:
                unique_words[keyword]['count'] += 1
                unique_words[keyword]['review_id'].append(keys[index]['rev_id'])
                unique_words[keyword]['sentence_id'].append(keys[index]['sentence_id'])
            else:
                unique_words[keyword] = {}
                unique_words[keyword]['count'] = 1
                unique_words[keyword]['review_id'] = [keys[index]['rev_id']]
                unique_words[keyword]['sentence_id'] = [keys[index]['sentence_id']]
            keyword_count += 1
            list_keywords = []
            stop_count = 0
            for feature in sorted(unique_words, key=unique_words.get, reverse=True):
                data = {}
                data['keyword'] = feature
                if stop_count == 0:
                    clusterinfo['feature'] = feature
                data['sentence_id'] = unique_words[feature]['sentence_id']
                data['review_id'] = unique_words[feature]['review_id']
                helpful_vote=0
                for index_rev in range(0,len(data['review_id'])):
                    if helpful[data['review_id'][index_rev]]>=helpful_vote:
                        helpful_vote=helpful[data['review_id'][index_rev]]
                        helpful_rev=index_rev
                #query_rev=Query(db_2, selector={'review_id':data['review_id'][helpful_rev]})
                #helpful_review=query_rev.result[0][0]
                #print "\n\n"
                #print helpful_rev
                sent_id=data['sentence_id'][helpful_rev]
                helpful_review=local_dump[data['review_id'][helpful_rev]]

                ##cause of split reviews-to remove
                sent_id=sent_id-helpful_review[0][0]['seqno']
                if sent_id>0:
                    excerpt=helpful_review[0][sent_id-1]['sentence']+helpful_review[0][sent_id]['sentence']
                else:
                    excerpt=helpful_review[0][sent_id]['sentence']
                if sent_id<len(helpful_review[0])-1:
                    excerpt=excerpt+helpful_review[0][sent_id+1]['sentence']
                #print helpful_review[sent_id]
                #print excerpt
                data['excerpt']=excerpt

                data['count'] = unique_words[feature]['count']
                list_keywords.append(data)
                stop_count += 1
                if stop_count == 3:
                    break
            if keys[index]['sentiment'][0][0] == 'positive':
                    pos += 1
            if keys[index]['sentiment'][0][0] == 'neutral':
                    neutral += 1
            if keys[index]['sentiment'][0][0] == 'negative':
                    neg += 1
        clusterinfo['keywords'] = list_keywords
        clusterinfo['sentiments'] = {}
        clusterinfo['sentiments']['positive'] = pos
        clusterinfo['sentiments']['negative'] = neg
        clusterinfo['sentiments']['neutral'] = neutral
        clusterinfo['keyword_count'] = keyword_count
        cluster_data.append(clusterinfo)
    return cluster_data


def cluster(doc, db, asin):
    SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'
    DATABASE = 'amazon_data'
    USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
    PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'

    server = cloudant.client.Cloudant(USERNAME, PASSWORD, url=SERVER)
    server.connect()
    db = server[DATABASE]
    query = Query(db, selector={'asin': asin, 'type':['review']},fields=["_id", "helpful"])
    meta = Query(db, selector={'asin': asin, 'type': ['metadata']})
    meta = meta.result[0][0]
    name = ''
    if 'title' in meta:
        name = meta['title']
    rev_id = []
    helpful={}
    for data in query.result:
        rev_id.append(data['_id'])
        if 'helpful' in data:
            helpful[data['_id']]=data['helpful'][0]
        else:
            helpful[data['_id']]=0

    temp = {}
    keys = []
    local_dump = {}
    for rev in rev_id:
        query_id = Query(db, selector={'review_id': rev, 'type': ['classified']})
        for i in query_id.result:
            if len(query_id.result[0]) == 0:
                continue
        for res in query_id.result[0]:
            text = res['review']
            local_dump[res['review_id']] = text
            for obj in text[0]:
                if 'Feature' in obj:
                    feature = obj['Feature']
                    for data in feature:
                        if 'name' in data:
                            temp = {}
                            temp['word'] = data['name']
                            if 'sentiment' in data:
                                temp['sentiment'] = data['sentiment']
                            else:
                                temp['sentiment'] = ['neutral']
                            temp['rev_id'] = res['review_id']
                            temp['sentence_id'] = obj['seqno']
                            keys.append(temp)

    modelname = 'sample_model'
    cwd = os.getcwd()
    model = word2vec.Word2Vec.load_word2vec_format(cwd+ '/' + modelname+'.bin', binary=True)
    [vecs, mapping] = generate_vectors(keys, model)
    clusters = cluster_try(vecs)
    cluster_data = []
    features = create_json(clusters, cluster_data, mapping, keys, helpful, local_dump)
    features = sorted(features, key=lambda k: k['keyword_count'], reverse=True)

    featureDict = {}
    featureDict['features'] = features[:10]
    featureDict['product_name'] = name
    return featureDict
