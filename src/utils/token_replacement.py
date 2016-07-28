import requests
import ast
import re
import nltk


def get_entities(review):
    split = {}
    url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=e21cc89b-125b-43e7-b13f-9e4112929c02&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json&sentiment=1"
    if len(review) > 5024:
        mid = find_middle(review)
        while mid >= 5024:
            mid = find_middle(review[:mid])
        review = review[:mid]
        half = review[mid:]
        split = get_entities(half)
    f = requests.get(url, params={'text': review})
    response = f.content
    response = ast.literal_eval(response)
    if split != {}:
        if 'entities' in split and 'entities' in response:
            response['entities'] = response['entities'] + split['entities']
            response['text'] = response['text'] + split['text']
        elif 'entites' in split and 'entities' not in response:
            response['entities'] = split['entities']
    return response


def find_middle(text):
        generator = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
        sequences = list(generator)
        mid_sentence = len(sequences)/2
        middle_char = sequences[mid_sentence][1]
        middle_char = int(middle_char) + 1
        return middle_char

def token_replacement(review_text):

    entity_info = get_entities(review_text)
    entity_info = avg_sentiment(entity_info)
    entities = []
    if 'entities' in entity_info:
        entities = entity_info['entities']
    sentences = nltk.tokenize.sent_tokenize(review_text)
    result = []
    sentence_dict = {}
    seq_no = 0
    i=seq_no
    dict={}
    for sentence in sentences:
        dict={}
        sentence_dict[sentence]=i-seq_no

        dict['sentence']=sentence
        dict['seqno']=i
        i+=1
        for entity in entities:
            #print entity
            token=entity['text']
            token = re.escape(token)
            if re.search(r'\b%s\b' % token, sentence) is not None:
                classification = "<" + entity['type'] + ">"
                re.sub(r'\\ ',' ',token)
                sentence = re.sub(r'\b%s\b' % token, classification, sentence)

                dict['replaced_sentence'] = dict['replaced_sentence'] + sentence
        result.append(dict)
    #print sentence_dict
    #print result

    return dict['replaced_sentence']

def avg_sentiment(review):
    sentiments = []
    if 'entities' in review:
        entities = review['entities']

        for sentence in entities:
            sentiments.append({'name':sentence['text'], 'sentiment':sentence['sentiment']['type'], 'done':False})
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
                            pos +=1
                        elif other['sentiment'] == 'negative':
                            neg +=1
                        elif other['sentiment'] == 'neutral':
                            neutral +=1
                if pos == max(pos,neg,neutral):
                    most = 'positive'
                elif neg == max(pos, neg, neutral):
                    most = 'negative'
                elif neutral == max(pos, neg, neutral):
                    most = 'neutral'

                for entity in entities:
                    if entity['text'] == text:
                        entity['sentiment']['type'] = [most]
    return review
#print token_replacement('This TV has good picture quality and this radio has good sound. I bought it for 500 dollars. I like this TV. I do not like the radio.');
