from watson_developer_cloud import NaturalLanguageClassifierV1
import csv
import sys, os

sys.path.insert(0, os.path.abspath('..'))
from utils import token_replacement as tr
from utils import classify as clf

TEST_SET_FILE = 'test_set.csv'
verbose = True

read = open(TEST_SET_FILE, 'rb')
reader = csv.reader(read)

confusion_matrix = {}
num_correct = 0
total = 0
for row in reader:
	sentence = row[0]
	correct_class = row[1]
	total += 1
	correct = False
	token = tr.token_replacement(sentence)
	classification = clf.classify(token)
	if(classification in correct_class):
		num_correct += 1
		correct = True
	if(verbose):
		print(sentence + " --> " + token)
		print("EXPECTED: " + correct_class + " / ACTUAL: " + classification)
		if(correct):
			print("CORRECT!")
		else:
			print("WRONG!")
		print("-" * 30)

print("CORRECT: " + str(num_correct) + "/" + str(total) + " (" + str(num_correct/float(total)*100) + ")")
read.close()