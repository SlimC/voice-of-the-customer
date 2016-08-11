import cloudant
from cloudant.query import Query
from gensim.models import word2vec
import logging
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


SERVER = ''  # Replace with your server URL
DATABASE = ''  # Replace with the name of the database
USERNAME = ''  # Replace with the username from your credentials for the NLC
PASSWORD = ''
DESIGN = ''    # Replace with the name of the design document that contains
                # the view. This should be of the form '_design/XXXX'
VIEW = ''      # Replace with the view from your database to poll,
               # this should take the form of view_file/view and should return
               # the text to classify as the value field and what you would
               # like to call it as the key
DESTINATION = ''  # Replace with correct name for output file (Must be *.csv)
CLASS_NAME = ''  # Replace with the name of the class to cluster


server = cloudant.client.Cloudant(USERNAME, PASSWORD, url=SERVER)
server.connect()
db = server[DATABASE]
query = Query(db, selector={'asin': 'B0042A8CW2'}, fields=["_id", "helpful"])


def generate_vectors(features):
    vecs = []
    mapping = []
    count = 0
    for line in features:
            print line
            words = line['word'].split()
            vec = []
            flag = 0
            for word in words:
                    if word in model:
                            if len(vec) > 1:
                                    vec = vec + model[word]
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

# features and stuff- array of json
# cluster features
# sentiment aggregation
# final json


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
                        sim = np.dot(vecs[i],
                                     clusterVec[j]) / \
                                     (np.linalg.norm(
                                      clusterVec[j]) * np.linalg.norm(vecs[i]))
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


def create_json(clusters, cluster_data, mapping):
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
                unique_words[keyword]['review_id'].append(
                                                    keys[index]['rev_id'])
                unique_words[keyword]['sentence_id'].append(
                                                    keys[index]['sentence_id'])
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
                # section to get most helpful review
                helpful_vote = 0
                for index_rev in range(0, len(data['review_id'])):
                    if helpful[data['review_id'][index_rev]] >= helpful_vote:
                        helpful_vote = helpful[data['review_id'][index_rev]]
                        helpful_rev = index_rev
                sent_id = data['sentence_id'][helpful_rev]
                helpful_review = local_dump[data['review_id'][helpful_rev]]

                sent_id = sent_id-helpful_review[0]['seqno']
                if sent_id > 0:
                    excerpt = helpful_review[sent_id-1]['sentence'] + \
                        helpful_review[sent_id]['sentence']
                else:
                    excerpt = helpful_review[sent_id]['sentence']
                if sent_id < len(helpful_review)-1:
                    excerpt = excerpt+helpful_review[sent_id+1]['sentence']
                data['excerpt'] = excerpt

                ####
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


rev_id = []
helpful = {}
for data in query.result:
    rev_id.append(data['_id'])
    if 'helpful' in data:
        helpful[data['_id']] = data['helpful'][0]
    else:
        helpful[data['_id']] = 0
print rev_id
print helpful


temp = {}
keys = []
local_dump = {}
for rev in rev_id:
    query_id = Query(db, selector={'review_id': rev})
    if len(query_id.result[0]) == 0:
        continue
    for res in query_id.result[0]:
        text = res['review']
        local_dump[res['review_id']] = text
        for obj in text:
            if CLASS_NAME in obj:
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

model = word2vec.Word2Vec.load_word2vec_format(modelname+'.bin', binary=True)

[vecs, mapping] = generate_vectors(keys)
clusters = cluster_try(vecs)

cluster_data = []
features = create_json(clusters, cluster_data, mapping)
features = sorted(features, key=lambda k: k['keyword_count'], reverse=True)

output_dict = {}
output_dict['product_id'] = 'sss'  # TODO: What is???
output_dict['features'] = features[:10]
