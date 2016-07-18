import requests
import ast
import pprint
import re
pp = pprint.PrettyPrinter(depth=6)
import nltk 

def get_relations(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=bbb894cf-003c-4000-9772-23e4860b3034&apikey=7e476d77ac23fabfcbf51a3a32c8d8faf6e9594b&outputMode=json"
	#url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=ae997404-c8d5-433a-995c-dceeacf22e34&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	print response
	return response

def get_entities(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=bbb894cf-003c-4000-9772-23e4860b3034&apikey=7e476d77ac23fabfcbf51a3a32c8d8faf6e9594b&outputMode=json&sentiment=1"
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
			text = re.replace(r"\b%s\b" % token, classification, text,count=1)
	return text

def token_replacement(review_text):
	review = get_relations(review_text)
	entity_info = get_entities(review_text)
	entities = []
	if 'entities' in entity_info:
		entities=entity_info['entities']
	sentences = nltk.tokenize.sent_tokenize(review_text)
	result=[]
	sentence_dict={}
	#print entities
	#print sentences
	i=0
	dict={}
	for sentence in sentences:
		dict={}
		sentence_dict[sentence]=i
		
		dict['sentence']=sentence
		dict['seqno']=i
		i+=1
		for entity in entities:
			#print entity
			token=entity['text']
			temp={}
			words=sentence.split()
			print words
			if token in words:
				#print "found"
				#print token+" "+sentence
				test={}
				test['name']=token
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
				temp_dict['name']=text['arguments'][0]['entities'][0]['text']
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
	return result
			
				
#print token_replacement('This TV has good picture quality and this radio has good sound. I bought it for 500 dollars. I like this TV. I do not like the radio.');
