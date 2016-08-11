'''
Takes a csv file with one record per line, uses the alchemy languag API to find
keywords and then replaces the keywords of the record with the name of the
class of the keywords. The end result is a generalized sentence.
Must change location of input .csv and output .csv
'''
import csv
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from utils import token_replacement as t

read = open('', 'rb')      # Replace with location of .csv file to classify
write = open('', 'wb')     # Replace with output file location

reader = csv.reader(read)
writer = csv.writer(write)

for row in reader:
    token = t.token_replacement_entities(row[0])
    writer.writerow([token, row[1], row[2]])

read.close()
write.close()
