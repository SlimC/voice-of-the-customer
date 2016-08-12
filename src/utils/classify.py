import json
from watson_developer_cloud import NaturalLanguageClassifierV1

CLF_USERNAME = ''  # Replace with the username from your credentials for NLC
CLF_PASSWORD = ''  # Replace with the password from your credentials for NLC
CLASSIFIER_JSON = '../../data/classifier_ids.json'  # Location of classifiers

# Retrieve Classifier ID's
with open(CLASSIFIER_JSON) as classifier_ids:
    classifierTree = json.load(classifier_ids)

nlc = NaturalLanguageClassifierV1(username=CLF_USERNAME, password=CLF_PASSWORD)

# TODO Make general, do not bind to our NLC classes

def classify(review):
    # classifierTree holds all of the layers and they are referenced by tierX where X is the layer number
    resp = nlc.classify(classifierTree['tier1'], review)
    classification = resp["top_class"]
    # If an output of tier1 is to be fed into tier2, this is how it is done
    if(classification == "Product"):
        resp = nlc.classify(classifierTree['tier2'], review)
        classification = resp["top_class"]
        # this is an example of feeding another output into tier3
        if(classification == "Feature"):
            resp = nlc.classify(classifierTree['tier3'], review)
            classification = resp["top_class"]
    return classification

# Returns the final classifications possible from the classifier architecture
def getClasses():
    return ["Comparison", "Sentiment", "Customer Service", "Other", "Price",
            "Issue", "Enhancement", "Feature"]
