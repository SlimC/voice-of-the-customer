import json
from watson_developer_cloud import NaturalLanguageClassifierV1

CLF_USERNAME = 'e561bc30-d294-41f4-8b47-39fc6bc29917'												#Replace with the username from your credentials for the NLC
CLF_PASSWORD = 'XH8pYnsYfClv'												#Replace with the password from your credentials for the NLC
CLASSIFIER_JSON = '../../data/classifier_ids.json'

# Retrieve Classifier ID's
with open(CLASSIFIER_JSON) as classifier_ids:
    classifierTree = json.load(classifier_ids)

nlc = NaturalLanguageClassifierV1(username = CLF_USERNAME, password = CLF_PASSWORD)

def classify(review):
	for line in review['review']:
		sentence = ""
		if('replaced_sentence' in line):
			sentence = line['replaced_sentence']
		else:
			sentence = line['sentence']
		resp = nlc.classify(classifierTree['tier1'],sentence)
		classification = resp["top_class"]
		line["layer1type"] = classification
		if(classification == "Product"):
			resp = nlc.classify(classifierTree['tier2'],sentence)
			classification = resp["top_class"]
			line["layer2type"] = classification
			if(classification != "Price"):
				resp = nlc.classify(classifierTree['tier3'],sentence)
				classification = resp["top_class"]
				line["layer3type"] = classification
			else:
				line["layer3type"] = ""
		else:
			line["layer2type"] = ""
			line["layer3type"] = ""
    review['type'] = ['classified']
    return review
