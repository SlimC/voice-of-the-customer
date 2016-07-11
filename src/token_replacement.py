import requests
import ast
import pprint
pp = pprint.PrettyPrinter(depth=6)

def get_relations(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=8f03f142-af7f-4487-be47-371fc3262705&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	return response

def get_entities(review)
	url = "http://access.alchemyapi.com/calls/text/TextGetRankedNamedEntities?showSourceText=1&model=8f03f142-af7f-4487-be47-371fc3262705&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json&sentiment=1"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	return response

def token_replacement_entities(reivew):
	review = get_entities(review)
	if 'entities' in review:
		entities = review['entities']
		text = review['text']
		for i in entities:
			token = i['text']
			count = i['count']
			classification = "<" + i['type'] + ">"
			text = text.replace(token,classification,count)
	return text

def token_replacement_relations(review):
	review = get_relations(review)
	if 'typedRelations' in review:
		types = review['typedRelations']
		text = review['text']
		standard = ""
		previous = ""
		new_sentence = True
		review_text_mod = ""
		flip = True
		sentence_dict={}
		prev_dict={}
		if types != []:
			count=0
			result=[]
			for sentence in types:
				#dict={}
				review_text = sentence['sentence']
				#dict['sentence']=review_text
				if review_text != standard:
					previous = standard
					standard = review_text
					new_sentence = True
					dict={}
					sentence_dict[standard]=count
					dict['sentence']=standard
					dict['seqno']=count
					print "\ndict\n"
					print dict
					text = text.replace(previous, review_text_mod, 1)
					count+=1
					#if count>1:
					result.append(prev_dict)
				else:
					new_sentence = False
					dict=result[sentence_dict[review_text]]
					review_text = review_text_mod
				temp_dict={}
				temp_dict['hasrel']=sentence['type']
				for entity in sentence['arguments']:
					for i in entity['entities']:
						token = i['text']
						temp_dict[entity['part']]=token
						if entity['part']=='first':
							if i['type'] in dict:
								dict[i['type']].append(temp_dict)
							else:
								dict[i['type']]=[]
                                dict[i['type']].append(temp_dict)
						else:
							sec_dict={}
							sec_dict['name']=i['text']
							if i['type'] in dict:
                                dict[i['type']].append(sec_dict)
                            else:
								dict[i['type']]=[]
                                dict[i['type']].append(sec_dict)
						classification = "<" + i['type'] + ">"
						if flip:
							review_text_mod = review_text.replace(token,classification,1)
							flip = False
						else:
							review_text_mod = review_text_mod.replace(token,classification,1)
							flip = True
				dict['reversed_sentence']=review_text_mod
				#print temp_dict
				print "final dict"
				print dict
				prev_dict=dict
				result[sentence_dict[sentence['sentence']]]=dict
				#result.append(dict)
				print "new"
				#print sentence_dict
		pp.pprint(result)
		text = text.replace(standard,review_text_mod,1)
		return text
		#pp.print(result
	else: 
		return review


print token_replacement('This TV has good picture quality and this radio has good sound. I bought it for 500 dollars');
