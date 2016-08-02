import requests
import ast
import re
import nltk

apikey = 'ffd7397f4be657f7740a84038f903271b2707a11'
modelId = '1ef79b92-8974-48cf-8a54-bfec9059e14f'

def get_relations(review):
    split = {}
    url = "https://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=" + modelId + "&apikey=" + apikey + "&outputMode=json"
    if len(review) > 5024:
        mid = find_middle(review)
        while mid >= 5024:
            mid = find_middle(review[:mid])
        half = review[mid:]
        review = review[:mid]
        split = get_relations(half)
    f = requests.get(url, params={'text': review})
    response = f.content
    response = ast.literal_eval(response)
    if split != {}:
        if 'typedRelations' in response and 'typedRelations' in split:
            response['typedRelations'] = response['typedRelations'] + split['typedRelations']
            response['text'] = response['text'] + split['text']
        elif 'typedRelations' in split and not 'typedRelations' in response:
            response['typedRelations'] = split['typedRelations']
    print response
    return response

def get_entities(review):
    split = {}
    url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=" + modelId + "&apikey=" + apikey + "&outputMode=json&sentiment=1"
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
        elif 'entites' in split and not 'entities' in response:
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
            if i['type']=='Descriptor':
               continue
            token = re.escape(token)
            re.sub(r'\\ ',' ',token)
            text = re.sub(r"\b%s\b" % token, classification, text,count=1)
    return text

def find_middle(text):
        generator = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
        sequences = list(generator)
        mid_sentence = len(sequences)/2
        middle_char = sequences[mid_sentence][1]
        middle_char = int(middle_char) + 1
        return middle_char


#print token_replacement('This TV has good picture quality and this radio has good sound. I bought it for 500 dollars. I like this TV. I do not like the radio.');
