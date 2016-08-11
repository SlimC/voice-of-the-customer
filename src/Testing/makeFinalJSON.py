import json
import cloudant
from watson_developer_cloud import AlchemyLanguageV1
from cloudant.query import Query

JSON_FILE = "./Model_Clustering.JSON"
outputJSON = {
    "product_name": "",
    "product_id": None,
    "features": [],
    "issues": {
        "percentage": 0,
        "review_ids": []
    },
    "customer_service": {
        "sentiment": {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
    }
}

SERVER = ''  # Replace with your server URL
DATABASE = ''  # Replace with the name of the database
USERNAME = ''  # Replace with the username from your credentials for the NLC
PASSWORD = ''  # Replace with the name of the database
AL_KEY = ''  # Replace with your alchemy language API key

server = cloudant.client.Cloudant(USERNAME, PASSWORD, url=SERVER)
server.connect()
db = server[DATABASE]

#Get all data from db
query = Query(db, selector={'type': ['clustered']})
data = query.result

reviews = []
for review in data:
    reviews.append(review)

with open('review_data.txt') as outfile:
    reviews = json.load(outfile)

alchemy = AlchemyLanguageV1(api_key=AL_KEY)

total = 0
for review in reviews:
    for line in review["review"]:
        total = total + 1
        if(line["layer3type"] == "Issue"):
            outputJSON["issues"]["percentage"] = \
                outputJSON["issues"]["percentage"] + 1
            outputJSON["issues"]["review_ids"].append(review["review_id"])
        if(line["layer2type"] == "Customer Service"):
            sentiment = alchemy.sentiment(text=line["sentence"])["docSentiment"]["type"]
            outputJSON["customer_service"]["sentiment"][sentiment] = \
                outputJSON["customer_service"]["sentiment"][sentiment] + 1

outputJSON["issues"]["percentage"] = \
    outputJSON["issues"]["percentage"]/float(total)*100
customer_service_total = 0
for sentiment in outputJSON["customer_service"]["sentiment"]:
    customer_service_total = customer_service_total + \
        outputJSON["customer_service"]["sentiment"][sentiment]

if(customer_service_total > 0):
    for sentiment in outputJSON["customer_service"]["sentiment"]:
        outputJSON["customer_service"]["sentiment"][sentiment] = \
            outputJSON["customer_service"]["sentiment"][sentiment] / \
            float(customer_service_total)*100

with open(JSON_FILE) as features:
    productFeatures = json.load(features)


featureArray = productFeatures["features"]
total = 0
for item in featureArray:
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
        feature["sentiments"][sent] = feature["sentiments"][sent] / \
            float(item["keyword_count"])*100
    outputJSON["features"].append(feature)

for item in outputJSON["features"]:
    item["percentage"] = item["percentage"]/float(total)*100

outputJSON['type'] = ['final']
db.create(outputJSON)
