import csv
import sys, os

sys.path.insert(0, os.path.abspath('..'))
from utils import token_replacement as t

read = open('ground_truth_layer1.csv','rb') ##replace with correct filenames
write = open('ground_truth_layer1_replace.csv','wb')     ##replace with correct filenames

reader = csv.reader(read)
writer = csv.writer(write)

for row in reader:
	token = t.token_replacement(row[0])
	writer.writerow([token,row[1]])
	
read.close()
write.close()