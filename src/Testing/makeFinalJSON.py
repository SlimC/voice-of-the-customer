import json

JSON_FILE = "./Model_Clustering.JSON"
outputJSON = {
	"product_name":"",
	"product_id":None,
	"features":[],
	"issues":{},
	"customer_service":{}
}

with open(JSON_FILE) as features:    
    productFeatures = json.load(features)

featureArray = productFeatures["features"]
for item in featureArray:
	#print(json.dumps(item,indent=2))
	feature = {}
	feature["group_name"] = item["group-name"]
	feature["percentage"] = 9
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