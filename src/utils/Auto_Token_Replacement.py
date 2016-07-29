import csv
import sys, os

#sys.path.insert(0, os.path.abspath('..'))
import token_replacement as t
#dir = os.path.dirname(__file__)
#print "directory is"
#print dir
read = open('televisions.csv','rb') ##replace with correct filenames
write = open('televisions_replace_no_descriptors.csv','wb')     ##replace with correct filenames

reader = csv.reader(read)
writer = csv.writer(write)

for row in reader:
	token = t.token_replacement_entities(row[0])
	writer.writerow([token,row[1],row[2]])
	
read.close()
write.close()
