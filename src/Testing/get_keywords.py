import nltk
import cloudant
import requests 
import csv
import sys
import extract_keywords
from cloudant.query import Query
SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'													#Replace with your server URL
DATABASE = 'amazon_data'												#Replace with the name of the database
USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'												#Replace with the username from your credentials for the NLC
PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'	
DESIGN = 'names'													#replace with the name of the design document that contains the view. This should be of the form '_design/XXXX'
VIEW = 		'asinview'												#Replace with the view from your database to poll, this should take the form of view_file/view and should return the text to classify as the value field and what you would like to call it as the key
DESTINATION = 'out1.csv'															#Replace with correct name for output file (NOTE must be *.csv)

#query = Query(my_database, selector={'_id': {'$gt': 0},})
server = cloudant.client.Cloudant(USERNAME,PASSWORD,url=SERVER)
server.connect()
db = server[DATABASE]
query = Query(db, selector={'asin':'B00BCGRZ04'})

#query = db.get_view_result(DESIGN,VIEW)
#file = open(DESTINATION, 'wb')
#writer = csv.writer(file)
count = sys.argv[1]
#print query.result[0]
count = int(count)

fp=open('unique_sample_TV_count.txt','w')
fw=open('unique_sample_TV_2.txt','w')
unique_clusters={}
for i in range(0,count):
	#text=query[i][0]['value']
	text=query.result[i][0]['reviewText']
	print text
	if text!=None:
		unique_clusters=extract_keywords.features(text,unique_clusters)
		print "\n unique clusters\n"
		print unique_clusters

for key in unique_clusters:
	fp.write(key+"?"+unique_clusters[key]+"\n")
	fw.write(key+"\n")		
#print query[0]
#print query[2]
'''
for doc in query.result:
        #print doc

        text=doc['reviewText']
        #print text
        review= token_replacement.token_replacement(text);

        dict={}
        #specify review id
        dict['review_id']=doc['_id']
        dict['review']=review
        print dict
        my_document=temp_database.create_document(dict)
'''
