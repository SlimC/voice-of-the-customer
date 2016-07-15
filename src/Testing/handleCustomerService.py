from cloudant.client import Cloudant
from cloudant.query import Query 
import json
from watson_developer_cloud import AlchemyLanguageV1

DB_USERNAME = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'													#Replace with your server URL
DB_PASSWORD = 'bfd53fe017adeea40cd4894bb29451ddff6805fc1b94a179eba4de8ef84b632f'
DB_ACCOUNT = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'
DATABASE = 'testdb'												#Replace with the name of the database
BULK_RATE = 100

AL_KEY = '7e476d77ac23fabfcbf51a3a32c8d8faf6e9594b'

alchemy = AlchemyLanguageV1(api_key=AL_KEY)

client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

query = Query(db, selector={'_id': {'$gt': 0},'review':{ '$exists':True }}) 
data = query.result

updated_reviews = []
for item in data:
	for keyword in item["review"]:
		if(keyword["layer2type"] == "Customer Service"):
			sentiment = alchemy.sentiment(text=keyword["sentence"])["docSentiment"]
			print(keyword["sentence"])
			print(sentiment)
			keyword["sentiment"] = sentiment
			print('-------------------')
			updated_reviews.append(item)
	if(len(updated_reviews) >= BULK_RATE):
		db.bulk_docs(updated_reviews)
		updated_reviews = []
db.bulk_docs(updated_reviews)