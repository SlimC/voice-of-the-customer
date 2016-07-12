
import couchdbkit
import json
from watson_developer_cloud import NaturalLanguageClassifierV1
import csv

tier1CSV = 'training_set1.csv'
tier2CSV = 'training_set2.csv'
tier3CSV = 'training_set3.csv'
USERNAME = 'e561bc30-d294-41f4-8b47-39fc6bc29917'
PASSWORD = 'XH8pYnsYfClv'
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

# Write the tiers with classifier id's to file for use later
with open(JSON_TARGET, 'w') as outfile:
    json.dump(classifierTree, outfile)

print("############# FULL CLASSIFIER TREE ##############")
print(json.dumps(classifierTree))