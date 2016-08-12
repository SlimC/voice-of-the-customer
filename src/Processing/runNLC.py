import json
from watson_developer_cloud import NaturalLanguageClassifierV1
import sys, os

sys.path.insert(0, os.path.abspath('..'))
from utils import classify as clf

def classify(review):
    for line in review['review'][0]:
        print(line)
        sentence = ""
        if('replaced_sentence' in line):
            sentence = line['replaced_sentence']
        else:
            sentence = line['sentence']
        if len(sentence) < 1024:
            line['layer1type'] = clf.classify(sentence)
        else:
            line['layer1type'] = 'Sentence too long to Classify'
    review['type'] = ['classified']
    return review