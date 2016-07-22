import requests
import ast
import re
import nltk

def get_relations(review):
    url = "https://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=e21cc89b-125b-43e7-b13f-9e4112929c02&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json"
    f = requests.get(url, params={'text':review})
    response = f.content
    response = ast.literal_eval(response)
    return response

def get_entities(review):
    url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=e21cc89b-125b-43e7-b13f-9e4112929c02&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json&sentiment=1"
    f = requests.get(url, params={'text':review})
    response = f.content
    response = ast.literal_eval(response)
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

def token_replacement(review_text,seq_no):
	print "\n\n text is \n"
	print review_text
	#data=[]
	#review_text=split_long_string(review_text,data)
	
	review = get_relations(review_text)
	entity_info = get_entities(review_text)
	entity_info = avg_sentiment(entity_info)
	entities = []
	if 'entities' in entity_info:
		entities=entity_info['entities']
	sentences = nltk.tokenize.sent_tokenize(review_text)
	result=[]
	sentence_dict={}
	#print entities
	#print sentences
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
			if re.search(r'\b%s\b' % token, sentence) is not None :
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
