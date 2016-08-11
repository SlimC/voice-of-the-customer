import csv

import token_replacement as t

read = open('/Users/mwassel/Downloads/headphones.csv','rb') ##replace with correct filenames
write = open('headphones_replace_no_desc.csv','wb')     ##replace with correct filenames

reader = csv.reader(read)
writer = csv.writer(write)

for row in reader:
	token = t.token_replacement_entities(row[0])
	writer.writerow([token,row[1], row[2]])

read.close()
write.close()
