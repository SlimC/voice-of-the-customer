import requests
import ast
import re
import nltk

sys.path.insert(0, os.path.abspath('..'))
from utils import token_replacement as t

def entity_extraction(review_text):
    print "\n\n text is \n"
    print review_text

    review = t.get_relations(review_text)
    entity_info = t.get_entities(review_text)
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
            temp={}
            token = re.escape(token)
            if re.search(r'\b%s\b' % token, sentence) is not None:
                print "found"
                #print token+" "+sentence
                test={}
                test['name']=token
                if 'sentiment' in entity:
                    test['sentiment']=[entity['sentiment']['type']]
                if entity['type'] in dict:
                    dict[entity['type']].append(test)
                else:
                    dict[entity['type']]=[]
                    dict[entity['type']].append(test)

                count=int(entity['count'])
                classification = "<" + entity['type'] + ">"
                token = re.escape(token)
                re.sub(r'\\ ',' ',token)
                sentence = re.sub(r'\b%s\b' % token, classification, sentence, count=count)

                dict['replaced_sentence']=sentence
        result.append(dict)
    #print sentence_dict
    #print result
    if 'typedRelations' in review:
        types = review['typedRelations']
        #print types
        if types != []:
            for text in types:
                #print text
                temp_dict={}
                temp_dict['hasrel']=text['type']
                #print text['arguments'][0]
                temp_dict['rel_name']=text['arguments'][0]['entities'][0]['text']
                type=text['arguments'][0]['entities'][0]['type']
                temp_dict['second']=text['arguments'][1]['entities'][0]['text']
                #print "temp_dict"
                #print temp_dict
                sentence=text['sentence']
                #print sentence
                #print "sentence dict"
                #print sentence_dict
                if sentence in sentence_dict:
                    dict=result[sentence_dict[sentence]]
                    #print "type"
                    #print dict[type]
                    if type in dict:
                        local=dict[type]
                        local.append(temp_dict)
                    else:
                        local=[temp_dict]
                        dict[type]=local

    #result = avg_sentiment(result)
    final_result=[result,i]
    return final_result

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
