import ast
import re
import nltk
import time
from watson_developer_cloud import alchemy_language_v1 as alchemy

apikey = ''  # Replace with your Alchemy Language API key
modelId = ''  # Replace with the model-id from Watson Knowledge Studio
alchemyapi = alchemy.AlchemyLanguageV1(api_key=apikey)


def get_relations(review):
    split = {}
    if len(review) > 5024:
        mid = find_middle(review)
        while mid >= 5024:
            mid = find_middle(review[:mid])
        half = review[mid:]
        review = review[:mid]
        split = get_relations(half)
    f = alchemyapi.typed_relations(text=review, model=modelId)
    response = f.content
    response = ast.literal_eval(response)

    while response['status'] == 'ERROR':
        if 'language' in response:
            if response['language'] != 'english':
                break
        time.sleep(60)

    if split != {}:
        if 'typedRelations' in response and 'typedRelations' in split:
            response['typedRelations'] = response['typedRelations'] + split['typedRelations']
            response['text'] = response['text'] + split['text']
        elif 'typedRelations' in split and 'typedRelations' not in response:
            response['typedRelations'] = split['typedRelations']
    return response


def get_entities(review):
    split = {}
    if len(review) > 5024:
        mid = find_middle(review)
        while mid >= 5024:
            mid = find_middle(review[:mid])
        review = review[:mid]
        half = review[mid:]
        split = get_entities(half)
    f = alchemyapi.entities(text=review, model=modelId, sentiment=True)
    response = f.content
    response = ast.literal_eval(response)
    while 'status' in response and response['status'] == 'ERROR':
        if 'language' in response:
            if response['language'] != 'english':
                break
        if response['statusInfo'] == 'content-is-empty':
            break
        print response
        time.sleep(60)

    if split != {}:
        if 'entities' in split and 'entities' in response:
            response['entities'] = response['entities'] + split['entities']
            response['text'] = response['text'] + split['text']
        elif 'entites' in split and 'entities' not in response:
            response['entities'] = split['entities']
    return response


def token_replacement_entities(review):
    processed = get_entities(review)
    if 'statusInfo' in processed:
        return review
    if 'entities' in processed:
        entities = processed['entities']
        text = processed['text']
        for i in entities:
            token = i['text']
            classification = "<" + i['type'] + ">"
            text = re.sub(r"\b%s\b" % token, classification, text, count=1)
    return text


def find_middle(text):
        generator = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
        sequences = list(generator)
        mid_sentence = len(sequences)/2
        middle_char = sequences[mid_sentence][1]
        middle_char = int(middle_char) + 1
        return middle_char


def token_replacement(review_text):
    review = get_relations(review_text)
    entity_info = get_entities(review_text)
    entity_info = avg_sentiment(entity_info)
    entities = []
    if 'entities' in entity_info:
        entities = entity_info['entities']
    sentences = nltk.tokenize.sent_tokenize(review_text)
    result = []
    sentence_dict = {}
    seq_no = 0
    i = seq_no
    entry = {}
    for sentence in sentences:
        entry = {}
        sentence_dict[sentence] = i-seq_no

        entry['sentence'] = sentence
        entry['seqno'] = i
        i += 1
        for entity in entities:
            token = entity['text']
            token = re.escape(token)
            token = re.sub(r'\\ ', ' ', token)
            if re.search(r'\b%s\b' % token, sentence) is not None:
                test = {}
                test['name'] = token
                if 'sentiment' in entity:
                    test['sentiment'] = [entity['sentiment']['type']]
                if entity['type'] in entry:
                    entry[entity['type']].append(test)
                else:
                    entry[entity['type']] = []
                    entry[entity['type']].append(test)

                count = int(entity['count'])
                classification = "<" + entity['type'] + ">"
                sentence = re.sub(r'\b%s\b' % token, classification, sentence, count=count)

                entry['replaced_sentence'] = sentence
        result.append(entry)
    if 'typedRelations' in review:
        types = review['typedRelations']
        if types != []:
            for text in types:
                temp_dict = {}
                temp_dict['hasrel'] = text['type']
                temp_dict['rel_name'] = text['arguments'][0]['entities'][0]['text']
                typed_entity = text['arguments'][0]['entities'][0]['type']
                temp_dict['second'] = text['arguments'][1]['entities'][0]['text']
                sentence = text['sentence']
                if sentence in sentence_dict:
                    entry = result[sentence_dict[sentence]]
                    if typed_entity in entry:
                        local = entry[typed_entity]
                        local.append(temp_dict)
                    else:
                        local = [temp_dict]
                        entry[typed_entity] = local

    final_result = [result, i]
    return final_result

def avg_sentiment(review):
    sentiments = []
    if 'entities' in review:
        entities = review['entities']

        for sentence in entities:
            if 'text' in sentence and 'sentiment' in sentence:
                sentiments.append({'name': sentence['text'],
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
