import json
from cloudant.client import Cloudant
from cloudant.query import Query 

JSON_FILE = "./Model_Clustering.JSON"
outputJSON = {
	"product_name":"",
	"product_id":None,
	"features":[],
	"issues":{},
	"customer_service":{}
}

DB_USERNAME = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'													#Replace with your server URL
DB_PASSWORD = 'bfd53fe017adeea40cd4894bb29451ddff6805fc1b94a179eba4de8ef84b632f'
DB_ACCOUNT = 'f097af24-3f84-4672-8b97-86dd54a78ef6-bluemix'
DATABASE = 'testdb'												#Replace with the name of the database

client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

#Get all data from db
query = Query(db, selector={'_id': {'$gt': 0},'review':{ '$exists':True }}) 
data = query.result

for review in data:
	

with open(JSON_FILE) as features:    
    productFeatures = json.load(features)

featureArray = productFeatures["features"]
for item in featureArray:
	#print(json.dumps(item,indent=2))
	feature = {}
	feature["group_name"] = item["group-name"]
	feature["percentage"] = None
	feature["keywords"] = []
	for i in range(len(item["keywords"])):
		elem = item["keywords"][i]
		keyword = {
			"name": elem,
			"review_ids": [item["review-ids"][i]]
		}
		feature["keywords"].append(keyword)
	feature["sentiments"] = {
		"positive": 81,
		"neutral": 3,
		"negative": 16
	}
	outputJSON["features"].append(feature)

print(json.dumps(outputJSON,indent=2))