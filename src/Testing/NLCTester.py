
import csv
import nltk
import couchdbkit
import json
from watson_developer_cloud import NaturalLanguageClassifierV1


SERVER = ''													#Replace with your server URL
DATABASE = ''												#Replace with the name of the database
USERNAME = ''												#Replace with the username from your credentials for the NLC
PASSWORD = ''												#Replace with the password from your credentials for the NLC
VIEW = 		''												#Replace with the view from your database to poll, this should take the form of /view_file/view and should return the text to classify
RESULTFILE = ''												#Replace with where to store the result file in csv format
CLASSIFIERID = ''											#Replace with the id of the classifier to use to classify


def split_long_string(token, nlc):
	if len(token) > 1024:
		sequences = nltk.tokenize.util.regexp_span_tokenize(token, r'\.')
		middle = find_middle(sequences)
		first_half = token[middle:].strip()
		second_half = token[:middle].strip()
		split_long_string(first_half,nlc)
		split_long_string(second_half,nlc)
	else:
		classes = classify_sentence(nlc, token)
		to_write = [token] + classes
		writer.writerow(to_write)



def find_middle(generator):
	sequences = list(generator)
	mid_sentence = len(sequences)/2
	middle_char = sequences[mid_sentence][1]
	middle_char = int(middle_char) + 1
	return middle_char


def classify_sentence(classifier, token):
	classes = classifier.classify(CLASSIFIERID, token)
	results = []
	for i in range(0, len(classes['classes'])):
		classname = classes['classes'][i].get('class_name')
		confidence = classes['classes'][i].get('confidence')
		results.append(classname)
		results.append(confidence)
	return results

server = couchdbkit.Server(SERVER)
db = server.get_or_create_db(DATABASE)
query = db.view(VIEW)

nlc = NaturalLanguageClassifierV1(username = USERNAME, password = PASSWORD)


data = json.loads(json.dumps(query.all()))

clean = open(RESULTFILE, 'w')
writer = csv.writer(clean)


for i in range(0, len(data)):
	id = data[i].get('id')
	sentences = nltk.tokenize.sent_tokenize(data[i].get('value'))
	for j in sentences:
		if len(j) > 1024:
			split_long_string(j, id, nlc)  #IMPORTANT: Comment out this line and uncomment the next if you do not want to split strings that are too long. (Useful if comparing index to index)
			#writer.writerow([j,"This sentence is too long to pass through the classifier"])
		else:
			classes = classify_sentence(nlc, j)
			to_write = [j] + classes + [id]
			writer.writerow(to_write)

clean.close()