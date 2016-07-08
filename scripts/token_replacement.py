def get_entities(review):
	url = "http://access.alchemyapi.com/calls/text/TextGetTypedRelations?showSourceText=1&model=8f03f142-af7f-4487-be47-371fc3262705&apikey=ffd7397f4be657f7740a84038f903271b2707a11&outputMode=json"
	f = requests.get(url, params={'text':review})
	response = f.content
	response = ast.literal_eval(response)
	return response


import requests
import ast

def token_replacement(review):
	review = get_entities(review)
	if 'typedRelations' in review:
		types = review['typedRelations']
		text = review['text']
		standard = ""
		previous = ""
		new_sentence = True
		review_text_mod = ""
		flip = True

		if types != []:
			for sentence in types:
				review_text = sentence['sentence']

				if review_text != standard:
					previous = standard
					standard = review_text
					new_sentence = True
					text = text.replace(previous, review_text_mod, 1)
				else:
					new_sentence = False
					review_text = review_text_mod

				for entity in sentence['arguments']:
					for i in entity['entities']:
						token = i['text']
						classification = "<" + i['type'] + ">"
						if flip:
							review_text_mod = review_text.replace(token,classification,1)
							flip = False
						else:
							review_text_mod = review_text_mod.replace(token,classification,1)
							flip = True

		text = text.replace(standard,review_text_mod,1)
		return text
	else: 
		return review