import ast
import re
import nltk
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
    if split != {}:
        if 'typedRelations' in response and 'typedRelations' in split:
            response['typedRelations'] = response['typedRelations'] + \
                split['typedRelations']
            response['text'] = response['text'] + split['text']
        elif 'typedRelations' in split and 'typedRelations' not in response:
            response['typedRelations'] = split['typedRelations']
    print response
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
            token = re.escape(token)
            re.sub(r'\\ ', ' ', token)
            text = re.sub(r"\b%s\b" % token, classification, text, count=1)
    return text


def find_middle(text):
        generator = nltk.tokenize.util.regexp_span_tokenize(text, r'\.')
        sequences = list(generator)
        mid_sentence = len(sequences)/2
        middle_char = sequences[mid_sentence][1]
        middle_char = int(middle_char) + 1
        return middle_char
