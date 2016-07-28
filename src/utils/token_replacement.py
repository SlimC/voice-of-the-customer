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
