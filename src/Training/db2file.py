import couchdbkit
import csv

SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'													#Replace with your server URL
DATABASE = 'amazon_data'												#Replace with the name of the database
USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'												#Replace with the username from your credentials for the NLC
PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'												#Replace with the password from your credentials for the NLC
VIEW = 		'names/namesAndAsin'												#Replace with the view from your database to poll, this should take the form of view_file/view and should return the text to classify as the value field and what you would like to call it as the key
DESTINATION = 'out.csv'															#Replace with correct name for output file (NOTE must be *.csv)

server = couchdbkit.Server(SERVER)
db = server.get_or_create_db(DATABASE)
query = db.view(VIEW)
file = open(DESTINATION, 'wb')
writer = csv.writer(file)


for q in query:
	print q
	if 'key' in q and q['key'] != None:
		title = q['key']
	else:
		title = "No Title"
	if 'value' in q and q['value'] != None:
		text = q['value']
	else:
		text = "No Text"
	writer.writerow([title,text])

file.close()