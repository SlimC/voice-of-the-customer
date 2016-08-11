import json
from watson_developer_cloud import NaturalLanguageClassifierV1

tier1CSV = ''  # Replace with location of layer 1 training data
tier2CSV = ''  # Replace with another location of layer 2 training data
USERNAME = ''  # Replace with username of NLC credentials
PASSWORD = ''  # Replace with password of NLC credentials
JSON_TARGET = '../../data/classifier_ids.json'  # Location to keep classifiers

classifierTree = {
    'tier1': '',
    'tier2': '',
    'tier3': ''
}

# Initialize classifier
nlc = NaturalLanguageClassifierV1(username=USERNAME, password=PASSWORD)

# Train tier 1 classifier
print("############# TIER 1 CLASSIFIER ##############")
with open(tier1CSV, 'rb') as training_data:
    classifier = nlc.create(
        training_data=training_data,
        name='tier1',
        language='en'
      )
print(json.dumps(classifier, indent=2))
classifierTree['tier1'] = classifier['classifier_id']

# Train tier 2 classifier
print("############# TIER 2 CLASSIFIER ##############")
with open(tier2CSV, 'rb') as training_data:
    classifier = nlc.create(
        training_data=training_data,
        name='tier2',
        language='en'
      )
print(json.dumps(classifier, indent=2))
classifierTree['tier2'] = classifier['classifier_id']


# Write the tiers with classifier id's to file for use later
with open(JSON_TARGET, 'w') as outfile:
    json.dump(classifierTree, outfile)

print("############# FULL CLASSIFIER TREE ##############")
print(json.dumps(classifierTree))
