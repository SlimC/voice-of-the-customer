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
	resp = nlc.classify(classifierTree['tier1'],review)
	classification = resp["top_class"]
	if(classification == "Product"):
		resp = nlc.classify(classifierTree['tier2'],review)
		classification = resp["top_class"]
		if(classification != "Price"):
			resp = nlc.classify(classifierTree['tier3'],review)
			classification = resp["top_class"]
	return classification

def getClasses():
	return ["Comparison", "Sentiment", "Customer Service", "Other", "Price", "Issue", "Enhancement", "Feature"]