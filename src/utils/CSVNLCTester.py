import csv
import nltk
from watson_developer_cloud import NaturalLanguageClassifierV1

CLASSIFIERID = '' ##Change to your classifier id

nlc = NaturalLanguageClassifierV1(username = '', password = '') ## Change to your credentials

data = open('', 'rb') ##Change to your input file, in csv format
datareader = csv.reader(data)

clean = open("", 'w') ##Change to your output file, in csv format
writer = csv.writer(clean)

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

for review in datareader:
	sentences = nltk.tokenize.sent_tokenize(review[0])
	for j in sentences:
		for j in sentences:
			if len(j) > 1024:
				split_long_string(j, nlc)  #IMPORTANT: Comment out this line and uncomment the next if you do not want to split strings that are too long. (Useful if comparing index to index)
				#writer.writerow([j,"This sentence is too long to pass through the classifier"])
			else:
				classes = classify_sentence(nlc, j)
				to_write = [j] + classes
				writer.writerow(to_write)

clean.close()
data.close()
