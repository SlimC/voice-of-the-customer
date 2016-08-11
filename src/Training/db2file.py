import cloudant
import csv

SERVER = ''      ''' Replace with your server URL'''
DATABASE = ''    ''' Replace with the name of the database'''
USERNAME = ''    ''' Replace with the username from your
                    credentials for the NLC'''
PASSWORD = ''    ''' Replace with the password from
                    your credentials for the NLC'''
DESIGN = ''      ''' Replace with the name of the design document that contains
                     the view. This should be of the form '_design/XXXX''''
VIEW = ''        ''' Replace with the view from your database to poll,
                    this should take the form of view_file/view and should
                    return the text to classify as the value field and what
                    you would like to call it as the key'''
DESTINATION = ''  ''' Replace with correct name for output
                    file (NOTE must be *.csv)'''

server = cloudant.client.Cloudant(USERNAME, PASSWORD, url=SERVER)
server.connect()
db = server[DATABASE]
query = db.get_view_result(DESIGN, VIEW)
file = open(DESTINATION, 'wb')
writer = csv.writer(file)


for q in query:
    print q[0]
    if 'key' in q[0] and q[0]['key'] is not None:
        title = q[0]['key']
    else:
        title = "No Title"
    if 'value' in q[0] and q[0]['value'] is not None:
        text = q[0]['value']
    else:
        text = "No Text"
    writer.writerow([title, text])

file.close()
