import json
from cloudant.client import Cloudant
from cloudant.query import Query
from watson_developer_cloud import AlchemyLanguageV1


JSON_FILE = "./Model_Clustering.JSON"
outputJSON = {
	"product_name": "",
	"product_id": None,
	"features": [],
	"issues": {
		"percentage": 0,
		"review_ids": []
	},
	"customer_service":{
		"sentiment": {
			"positive": 0,
			"neutral": 0,
			"negative": 0
		}
	}
}

DB_USERNAME = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'													#Replace with your server URL
DB_PASSWORD = 'bfd53fe017adeea40cd4894bb29451ddff6805fc1b94a179eba4de8ef84b632f'
DB_ACCOUNT = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'
DATABASE = 'testdb'												#Replace with the name of the database
AL_KEY = '7e476d77ac23fabfcbf51a3a32c8d8faf6e9594b'

#client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
#client.connect()
#db = client[DATABASE]

#Get all data from db
#query = Query(db, selector={'_id': {'$gt': 0},'review':{ '$exists':True }})
#data = query.result

#JSON_array = []
#for review in data:
#	print(review)
#	JSON_array.append(review)

def make_final(cluster):

	outputJSON = {
		"product_name": "",
		"product_id": None,
		"features": [],
		"issues": {
			"percentage": 0,
			"review_ids": []
		},
		"customer_service":{
			"sentiment": {
				"positive": 0,
				"neutral": 0,
				"negative": 0
			}
		}
	}

	alchemy = AlchemyLanguageV1(api_key=AL_KEY)

	reviewnums = set()

	for group in cluster'features']:
		for keywords in group['keywords']:
			for review_ids in keywords['review_id']:
				reviews.add(review_ids)

	reviews = []

	for i in range(0,len(reviews)):
		reviews[i] = db[reviewnums.pop()]

	total = 0
	for review in reviews:
		for line in review["review"]:
			total = total + 1
			if(line["layer3type"] == "Issue"):
				outputJSON["issues"]["percentage"] = outputJSON["issues"]["percentage"] + 1
				outputJSON["issues"]["review_ids"].append(review["review_id"])
			if(line["layer2type"] == "Customer Service"):
				sentiment = alchemy.sentiment(text=line["sentence"])["docSentiment"]["type"]
				#print(sentiment)
				outputJSON["customer_service"]["sentiment"][sentiment] = outputJSON["customer_service"]["sentiment"][sentiment] + 1

	outputJSON["issues"]["percentage"] = outputJSON["issues"]["percentage"]/float(total)*100
	customer_service_total = 0
	for sentiment in outputJSON["customer_service"]["sentiment"]:
		customer_service_total = customer_service_total + outputJSON["customer_service"]["sentiment"][sentiment]

	if(customer_service_total > 0):
		for sentiment in outputJSON["customer_service"]["sentiment"]:
			outputJSON["customer_service"]["sentiment"][sentiment] = outputJSON["customer_service"]["sentiment"][sentiment]/float(customer_service_total)*100

	featureArray = cluster["features"]
	total = 0
	for item in featureArray:
		#print(json.dumps(item,indent=2))
		feature = {}
		feature["group_name"] = item["feature"]
		feature["percentage"] = item["keyword_count"]
		total = total + item["keyword_count"]
		feature["sentiments"] = item["sentiments"]
		feature["keywords"] = []
		for i in range(len(item["keywords"])):
			elem = item["keywords"][i]
			keyword = {
				"name": elem["keyword"],
				"review_id": elem["review_id"],
				"sentence_id": elem["sentence_id"]
			}
			feature["keywords"].append(keyword)
		for sent in feature["sentiments"]:
			feature["sentiments"][sent] = feature["sentiments"][sent]/float(item["keyword_count"])*100
		outputJSON["features"].append(feature)

	for item in outputJSON["features"]:
		item["percentage"] = item["percentage"]/float(total)*100

	return outputJSON
