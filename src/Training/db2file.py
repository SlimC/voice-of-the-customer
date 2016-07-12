import cloudant
import csv

SERVER = 'https://1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com'													#Replace with your server URL
DATABASE = 'amazon_data'												#Replace with the name of the database
USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'												#Replace with the username from your credentials for the NLC
PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'												#Replace with the password from your credentials for the NLC
DESIGN = ''													#replace with the name of the design document that contains the view. This should be of the form '_design/XXXX'
VIEW = 		'names/namesAndAsin'												#Replace with the view from your database to poll, this should take the form of view_file/view and should return the text to classify as the value field and what you would like to call it as the key
DESTINATION = 'out.csv'															#Replace with correct name for output file (NOTE must be *.csv)

server = cloudant.client.Cloudant(USERNAME,PASSWORD,url=SERVER)
server().connect
db = server[DATABASE]
query = db.get_view_result(DESIGN,VIEW)
file = open(DESTINATION, 'wb')
writer = csv.writer(file)


for q in query:
	print q[0]
	if 'key' in q[0] and q[0]['key'] != None:
		title = q[0]['key']
	else:
		title = "No Title"
	if 'value' in q[0] and q[0]['value'] != None:
		text = q[0]['value']
	else:
		text = "No Text"
	writer.writerow([title,text])

file.close()