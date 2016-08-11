from cloudant.client import Cloudant
from cloudant.query import Query
import json
from watson_developer_cloud import NaturalLanguageClassifierV1

DB_USERNAME = ''  # Replace with your server URL
DB_PASSWORD = ''  # Replace with your DB password
DB_ACCOUNT = ''  # replace with your DB username
DATABASE = ''  # Replace with the name of the database

CLF_USERNAME = ''  # Replace with the username from your credentials for the NLC
CLF_PASSWORD = ''  # Replace with the password from your credentials for the NLC
CLASSIFIER_JSON = '../../data/classifier_ids.json'  # Location of classifiers

BULK_RATE = 100

# Retrieve Classifier ID's
with open(CLASSIFIER_JSON) as classifier_ids:
    classifierTree = json.load(classifier_ids)
print(classifierTree)

client = Cloudant(DB_USERNAME, DB_PASSWORD, account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

# mock Data
data = [{
   'review_id': 137,
   'review': [{'Descriptor': [{'name': 'good'}, {'name': 'good'}],
                'Feature': [{'name': 'picture quality'},
                            {'name': 'sound'},
                            {'first': 'picture quality',
                            'hasrel': 'hasQuality',
                            'second': 'good'},
                            {'first': 'picture quality',
                             'hasrel': 'hasQuality',
                             'second': 'good'}],
               'Product': [{'first': 'TV',
                           'hasrel': 'hasFeature',
                           'second': 'picture quality'},
                            {'first': 'TV', 'hasrel': 'hasFeature', 'second': 'sound'}],
               'replaced_sentence': 'This <Product> has <Descriptor> <Feature> and this radio has <Descriptor> <Feature>.',
               'sentence': 'This TV has good picture quality and this radio has good sound.',
               'seqno': 0
               },
 {'Consumer': [{'first': 'I', 'hasrel': 'owns', 'second': 'TV'}],
  'Feature': [{'name': '500 dollars'}],
  'Product': [{'name': 'TV'},
              {'first': 'TV',
               'hasrel': 'hasFeature',
               'second': '500 dollars'}],
  'replaced_sentence': '<Consumer> bought it for <Feature>',
  'sentence': 'I bought it for 500 dollars',
  'seqno': 1}],

'type':'review'
}]

query = Query(db, selector={'type': ["replaced"]})
data = query.result

nlc = NaturalLanguageClassifierV1(username=CLF_USERNAME, password=CLF_PASSWORD)

updated_reviews = []
for review in data:
    # Run tier 1 classification
    for line in review['review']:
        sentence = ""
        if('replaced_sentence' in line):
            sentence = line['replaced_sentence']
        else:
            sentence = line['sentence']
        resp = nlc.classify(classifierTree['tier1'], sentence)
        classification = resp["top_class"]
        line["layer1type"] = classification
        if(classification == "Product"):
            resp = nlc.classify(classifierTree['tier2'], sentence)
            classification = resp["top_class"]
            line["layer2type"] = classification
            if(classification != "Price"):
                resp = nlc.classify(classifierTree['tier3'], sentence)
                classification = resp["top_class"]
                line["layer3type"] = classification
            else:
                line["layer3type"] = ""
        else:
            line["layer2type"] = ""
            line["layer3type"] = ""
    review['type'] = ['classified']
    updated_reviews.append(review)
    if(len(updated_reviews) >= BULK_RATE):
        db.bulk_docs(updated_reviews)
        updated_reviews = []
db.bulk_docs(updated_reviews)
