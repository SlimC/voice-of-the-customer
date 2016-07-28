import csv
import sys, os

#sys.path.insert(0, os.path.abspath('..'))
import token_replacement as t
#dir = os.path.dirname(__file__)
#print "directory is"
#print dir
read = open('ground_truth_layer3.csv','rb') ##replace with correct filenames
write = open('ground_truth_layer3_replace.csv','wb')     ##replace with correct filenames

reader = csv.reader(read)
writer = csv.writer(write)

for row in reader:
	token = t.token_replacement_entities(row[0])
	writer.writerow([token,row[1]])
	
read.close()
write.close()
