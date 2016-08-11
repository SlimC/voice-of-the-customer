import requests
import ast
import pprint
import re
pp = pprint.PrettyPrinter(depth=6)
import nltk 

def get_relations(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=b6b78f7e-d035-48ba-9dff-f464154609dd&apikey=dd8e269c92c4149bbf3e3b81490de0de4378dcab&outputMode=json"
	#url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=ae997404-c8d5-433a-995c-dceeacf22e34&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	return response

def get_entities(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=a259053c-01e6-4fb9-a4e4-2377bb35b43f&apikey=dd8e269c92c4149bbf3e3b81490de0de4378dcab&outputMode=json&sentiment=1"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	print response
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

fp=open('sample_TV.txt','w')
fd=open('descriptors_TV.txt','w')
#fx=open('unique_sample_TV.txt','w')

def split_long_string(token, nlc):
        if len(token) > 1024:
                sequences = nltk.tokenize.util.regexp_span_tokenize(token, r'\.')
                middle = find_middle(sequences)
                first_half = token[middle:].strip()
                second_half = token[:middle].strip()
                split_long_string(first_half,nlc)
                split_long_string(second_half,nlc)
        else:
                classes = classify_sentence(nlc, token)
                to_write = [token] + classes
                writer.writerow(to_write)

def features(review_text,unique_clusters):
	fp.write("________________\n")
	fd.write("________________\n")
	print "\n obtained unique cluster"
	print unique_clusters
	#unique_clusters={}
	#fp.write("new review\n")
	print "review text"
	print review_text
	entity_info = get_entities(review_text)
	if 'entities' in entity_info:
                entities=entity_info['entities']
		for entity in entities:
			token=entity['text']
			if entity['type']=='Feature':
				if token in unique_clusters:
					unique_clusters[token]+=1
				else:
					unique_clusters[token]=0	
                        	fp.write(token+"\n")
			if entity['type']=='Descriptor':
                                        fd.write(token+"\n")
	#for token in unique_clusters:
	#	fx.write(token+"\n")
	return unique_clusters
