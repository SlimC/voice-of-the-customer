import nltk
import cloudant
import requests 
import csv
import sys

SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'													#Replace with your server URL
DATABASE = 'amazon_data'												#Replace with the name of the database
USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'												#Replace with the username from your credentials for the NLC
PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'	
DESIGN = 'names'													#replace with the name of the design document that contains the view. This should be of the form '_design/XXXX'
VIEW = 		'asinview'												#Replace with the view from your database to poll, this should take the form of view_file/view and should return the text to classify as the value field and what you would like to call it as the key
DESTINATION = ''															#Replace with correct name for output file (NOTE must be *.csv)

server = cloudant.client.Cloudant(USERNAME,PASSWORD,url=SERVER)
server.connect()
db = server[DATABASE]
query = db.get_view_result(DESIGN,VIEW)
file = open(DESTINATION, 'wb')
writer = csv.writer(file)
count = sys.argv[1]

if count == '':
	print "Please include how many reviews you want"
else:
	count = int(count)
	for i in range(0,count):
		review = query[i]
		sentences = nltk.tokenize.sent_tokenize(review[0]['value'])
		for sentence in sentences:
			writer.writerow([sentence])

file.close()