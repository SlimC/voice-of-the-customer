from cloudant.client import Cloudant
from cloudant.query import Query 
import json
from watson_developer_cloud import NaturalLanguageClassifierV1

DB_USERNAME = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'													#Replace with your server URL
DB_PASSWORD = 'bfd53fe017adeea40cd4894bb29451ddff6805fc1b94a179eba4de8ef84b632f'
DB_ACCOUNT =  'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'
DATABASE = 'testdb'												#Replace with the name of the database
VIEW = 		''												#Replace with the view from your database to poll, this should take the form of _design/view_file/_view/view and should return the text to classify

CLF_USERNAME = 'e561bc30-d294-41f4-8b47-39fc6bc29917'												#Replace with the username from your credentials for the NLC
CLF_PASSWORD = 'XH8pYnsYfClv'												#Replace with the password from your credentials for the NLC
CLASSIFIER_JSON = '../../data/classifier_ids.json'

# Retrieve Classifier ID's
with open(CLASSIFIER_JSON) as classifier_ids:    
    classifierTree = json.load(classifier_ids)
print(classifierTree)

client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

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

#TODO: need to get the data from the database still using cloudant query
query = Query(db,selector={"_id": {"$gt": 0}, "review":{"$exists": True}}) 
data = query.result

nlc = NaturalLanguageClassifierV1(username = CLF_USERNAME, password = CLF_PASSWORD)

for review in query.result:
	# Run tier 1 classification
	for line in review['review']:
		sentence = line['reversed_sentence']
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
	print(json.dumps(review,indent=2))