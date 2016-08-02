import couchdbkit
import json
from watson_developer_cloud import NaturalLanguageClassifierV1
import csv

tier1CSV = 'new train sets/training_layer1_replace_no_descriptor.csv'
tier2CSV = 'new train sets/training_layer2_replace_no_descriptor.csv'
#tier3CSV = 'training_set3.csv'
USERNAME = 'a6f087f2-73d6-4d33-bece-821ec3c5b96a'
PASSWORD = '8StZ2fxq0eFF'
JSON_TARGET = '../../data/classifier_ids.json'

classifierTree = {
	'tier1':'',
	'tier2':'',
	'tier3':''
}

# Initialize classifier
nlc = NaturalLanguageClassifierV1(username = USERNAME, password = PASSWORD)

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

'''
# Train tier 3 classifier
print("############# TIER 3 CLASSIFIER ##############")
with open(tier3CSV, 'rb') as training_data:
  classifier = nlc.create(
    training_data=training_data,
    name='tier3',
    language='en'
  )
print(json.dumps(classifier, indent=2))
classifierTree['tier3'] = classifier['classifier_id']
'''

# Write the tiers with classifier id's to file for use later
with open(JSON_TARGET, 'w') as outfile:
    json.dump(classifierTree, outfile)

print("############# FULL CLASSIFIER TREE ##############")
print(json.dumps(classifierTree))
