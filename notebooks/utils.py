#!/usr/bin/env python
#
# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

import re
import os
import nltk
import configparser
import numpy as np
from cloudant.query import Query
from watson_developer_cloud import AlchemyLanguageV1


def avg_sentiment(review):
    """
    Get the overall sentiment of a paragraph by looking
    at the sentiment that is mostly reflected on the
    sentences.
    Input: response from alchemy with sentiment output.
    Output: augmented json object with overall sentiment.
    """
    sentiments = []
    if 'entities' in review:
        entities = review['entities']
        for sentence in entities:
            if 'text' in sentence and 'sentiment' in sentence:
                sentiments.append({'name': sentence['text'], \
                    'sentiment': sentence['sentiment']['type'], 'done': False})
        for feature in sentiments:
            if not feature['done']:
                text = feature['name']
                pos = 0
                neg = 0
                neutral = 0
                most = ''
                for other in sentiments:
                    if other['name'] == text:
                        other['done'] = True
                        if other['sentiment'] == 'positive':
                            pos += 1
                        elif other['sentiment'] == 'negative':
                            neg += 1
                        elif other['sentiment'] == 'neutral':
                            neutral += 1
                if pos == max(pos, neg, neutral):
                    most = 'positive'
                elif neg == max(pos, neg, neutral):
                    most = 'negative'
                elif neutral == max(pos, neg, neutral):
                    most = 'neutral'
                for entity in entities:
                    if entity['text'] == text:
                        entity['sentiment']['type'] = [most]
    return review


def find_middle(text):
    """
    If the review is too long, this function will find
    the middle of it.
    Input: text to find the middle.
    Output: offset that represents the middle of the excerpt.
    """
    generator = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
    sequences = list(generator)
    mid_sentence = len(sequences)/2
    middle_char = sequences[mid_sentence][1]
    middle_char = int(middle_char) + 1
    return middle_char


def generate_vectors(features, model):
    """
    Generate word vectors based on learned model.
    Input: features identified and trained model.
    Output: word vectors.
    """
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
    """
    Create clusters of features based on word vectors.
    Input: word vectors.
    Output: dictionary containing cluster information.
    """
    cluster_vec = {}
    cluster_idx = {}
    no_of_clusters = 1
    cluster_idx[0] = [0]
    cluster_vec[0] = vecs[0]
    max_sim = 0.5
    index = 0
    for i in range(1, len(vecs)):
        flag = 0
        max_sim = 0.5
        for j in range(no_of_clusters):
            sim = 0.0
            try:
                sim = np.dot(vecs[i], cluster_vec[j])/\
                (np.linalg.norm(cluster_vec[j]) * np.linalg.norm(vecs[i]))
            except ArithmeticError:
                print "Error when calculating similarity of vectors."
            if sim > max_sim:
                flag = 1
                max_sim = sim
                index = j
            if flag == 0:
                cluster_idx[j+1] = [i]
                cluster_vec[j+1] = vecs[i]
                no_of_clusters += 1
            else:
                cluster_idx[index].append(i)
                cluster_vec[index] += vecs[i]
    return cluster_idx


def create_json(clusters, cluster_data, mapping, keys, helpful, local_dump):
    """
    Generate json object to be saved to the database document.
    Input: clusters and word vectors information.
    Output: json object to be saved to the database.
    """
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
                unique_words[keyword]['review_id'].append\
                (keys[index]['review_id'])
                unique_words[keyword]['sentence_id'].append\
                (keys[index]['sentence_id'])
            else:
                unique_words[keyword] = {}
                unique_words[keyword]['count'] = 1
                unique_words[keyword]['review_id'] = [keys[index]['review_id']]
                unique_words[keyword]['sentence_id'] = \
                [keys[index]['sentence_id']]
            keyword_count += 1
            list_keywords = []
            stop_count = 0
            for feature in sorted(unique_words, key=unique_words.get, \
            reverse=True):
                data = {}
                data['keyword'] = feature
                if stop_count == 0:
                    clusterinfo['feature'] = feature
                data['sentence_id'] = unique_words[feature]['sentence_id']
                data['review_id'] = unique_words[feature]['review_id']
                helpful_vote = 0
                for index_rev in range(0, len(data['review_id'])):
                    if helpful[data['review_id'][index_rev]] >= helpful_vote:
                        helpful_vote = helpful[data['review_id'][index_rev]]
                        helpful_rev = index_rev
                sent_id = data['sentence_id'][helpful_rev]
                helpful_review = local_dump[data['review_id'][helpful_rev]]

                ##cause of split reviews-to remove
                sent_id = sent_id-helpful_review[0][0]['seqno']
                if sent_id > 0:
                    excerpt = helpful_review[0][sent_id-1]['sentence']+\
                        helpful_review[0][sent_id]['sentence']
                else:
                    excerpt = helpful_review[0][sent_id]['sentence']
                if sent_id < len(helpful_review[0])-1:
                    excerpt = excerpt+helpful_review[0][sent_id+1]['sentence']

                data['excerpt'] = excerpt

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


def make_final(database, cluster):
    """
    Create a final json object compiling cluster information.
    Input: a cluster.
    Output: json object.
    """
    outputJSON = {"product_name": "",\
                  "product_id": None,\
                  "features": [],\
                  "issues": {"percentage": 0,\
                             "review_ids": []},\
                  "customer_service": \
                  {"sentiment": \
                       {"positive": 0,\
                        "neutral": 0,\
                        "negative": 0}}}

    #getting current directory
    curdir = os.getcwd()

    #loading credentials from .env file
    credFilePath = os.path.join(curdir, '..', '.env')
    config = configparser.ConfigParser()
    config.read(credFilePath)
    alchemy_key = AlchemyLanguageV1(api_key=\
                    config['ALCHEMY']['ALCHEMY_API_KEY'])

    alchemy = AlchemyLanguageV1(api_key=alchemy_key)

    reviewnums = set()
    reviews = []

    for group in cluster['features']:
        for keywords in group['keywords']:
            for review_ids in keywords['review_id']:
                reviewnums.add(review_ids)
    for i in range(0, len(reviewnums)):
        if len(reviewnums) > 0:
            num = reviewnums.pop()
            query = Query(database, selector=\
            {'review_id': num, 'type':'classified'})
            reviews.append(query.result[0])
    reviewnums.clear()
    total = 0
    for review in reviews:
        if review != []:
            for line in review[0]["review"]:
                total = total + 1
                if isinstance(line) == list:
                    line = line[0]
                if isinstance(line) == int:
                    continue
                if line["layer1type"] == "Issue":
                    outputJSON["issues"]["percentage"] = \
                        outputJSON["issues"]["percentage"] + 1
                    outputJSON["issues"]["review_ids"].\
                        append(review[0]["review_id"])
                if line["layer1type"] == "Customer Service":
                    sentiment = 'neutral'
                    try:
                        sentiment = alchemy.sentiment(text=\
                        line["sentence"])["docSentiment"]["type"]
                    except KeyError:
                        print "Unable to assess sentiment of: "+ \
                        str(line["sentence"])
                    outputJSON["customer_service"]["sentiment"][sentiment] \
                    = outputJSON["customer_service"]["sentiment"][sentiment] + 1
    if total > 0:
        outputJSON["issues"]["percentage"] = \
            round(outputJSON["issues"]["percentage"]/float(total)*100, 2)
    else:
        outputJSON["issues"]["percentage"] = 0
    customer_service_total = 0
    for sentiment in outputJSON["customer_service"]["sentiment"]:
        customer_service_total = customer_service_total + \
            outputJSON["customer_service"]["sentiment"][sentiment]

    if customer_service_total > 0:
        for sentiment in outputJSON["customer_service"]["sentiment"]:
            if customer_service_total > 0:
                outputJSON["customer_service"]["sentiment"][sentiment] =\
                    round(outputJSON["customer_service"]["sentiment"]\
                    [sentiment]/float(customer_service_total)*100, 2)
            else:
                outputJSON["customer_service"]["sentiment"][sentiment] = 0
    featureArray = cluster["features"]
    total = 0
    for item in featureArray:
        feature = {}
        feature["group_name"] = item["feature"]
        feature["percentage"] = item["keyword_count"]
        total = total + item["keyword_count"]
        feature["sentiments"] = item["sentiments"]
        feature["keywords"] = []
        for i in range(len(item["keywords"])):
            elem = item["keywords"][i]
            keyword = {
                "name": elem["keyword"],
                "review_id": elem["review_id"],
                "sentence_id": elem["sentence_id"]
            }
            feature["keywords"].append(keyword)
        for sent in feature["sentiments"]:
            feature["sentiments"][sent] = round(feature["sentiments"][sent]/\
            float(item["keyword_count"])*100, 2)
        outputJSON["features"].append(feature)

    for item in outputJSON["features"]:
        if total > 0:
            item["percentage"] = round(item["percentage"]/float(total)*100, 2)
        else:
            item["percentage"] = 0

    return outputJSON

def add_review(status):
    """
    Adds the flags on the tracker document.
    Input: tracker document.
    Output: sum of the switches.
    """
    cluster = status['cluster_switch']
    classify = status['classify_switch']
    replace = status['replace_switch']
    final = status['final_switch']
    finished = status['finished_switch']
    num = cluster + classify + replace + final + finished
    return num
