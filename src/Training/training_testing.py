'''
This script creates a training and testing split out of your data for you. It
can either be run interactivly by running the script witout arguments, or run
automatically with command line arguments.
The flags are:
    -l The location of the data, a directory of .txt or .json files or a .csv
        file
    -r Percentage of data to split into training
    -e Precentage of data to split into testing
    -j Field in .json that contains the text data. Only necessary if loading
        from a .json file. 
'''

import os
import numpy as np
import ast
import re
import csv
import sys
import getopt


def csv_handler(file, training, testing):
    ftest = open("testing_set.csv", "wb")
    ftrain = open("training_set.csv", "wb")
    wtest = csv.writer(ftest)
    wtrain = csv.writer(ftrain)

    rand = np.random.rand

    reader = csv.reader(f)

    for row in reader:
        if rand() < training:
            wtrain.writerow([row])
        else:
            wtest.writerow([row])

    ftest.close()
    ftrain.close()


def txt_handler(file, writer):

    text = file.read()
    writer.writerow([text])


def json_handler(file, writer, json_field):
    raw_text = file.read()

    try:
        processed_text = ast.literal_eval(raw_text)
        text = processed_text[json_field]
        writer.writerow([text])
    except:
        print "ERROR: Something wrong with .json file: " + file.name
flags = {}

if len(sys.argv) > 1:
    args = sys.argv[1:]
    opts = getopt.getopt(args, 'l:e:r:j:')
    for pair in opts:
        flags[pair[0]] = pair[1]


if len(sys.argv) > 1:
    print "Input the full path to your data"
    print "The data can be in the format of a .csv file (with one column" + \
        " and one text per line), or a directory of .json or .txt files."
    print "NOTE: If you are using a directory, please make sure your data" + \
        "is the only thing in the directory"
    location = raw_input("Data Location: ")
else:
    if '-l' in flags:
        location = flags['-l']
    else:
        print "ERROR: No file location. Did you use the -l" +\
            " flag to mark a file location?"

if re.match(r".\.csv$", location):
    try:
        f = open(location, 'rb')
        training = 0
        testing = 0
        if len(sys.argv) > 1:
            while training + testing != 100:
                print "What fraction would you like to use for training?" + \
                    " (We recommend 70%)"
                training = raw_input("Training (0-100): ")
                print "What fraction would you like to use for testing?" + \
                    " (We recommend 30%)"
                testing = raw_input("Testing (0-100): ")
                if training + testing != 100:
                    print "ERROR: Training and testing sets must equal 100%"
        else:
            if '-r' in flags and '-e' in flags:
                training = flags['-r']
                testing = flags['-e']
            else:
                print "ERROR: No training or testing split." + \
                    " Did you use the -r and -e flags to mark them?"

        training = float(training)/100
        testing = float(testing)/100

        csv_handler(f, training, testing)
        f.close()

    except (IOError):
        print "ERROR: File not found"

else:
    json_field = ""
    try:
        files = os.listdir(location)
        rand = np.random.rand
        total_docs = len(files)
        training = 0
        testing = 0
        if len(sys.argv) > 1:
            while training + testing != 100:
                print "What fraction would you like to use for training?" + \
                    " (We recommend 70%)"
                training = input("Training (0-100): ")
                print "What fraction would you like to use for testing?" + \
                    " (We recommend 30%)"
                testing = input("Testing (0-100): ")
                if training + testing != 100:
                    print "ERROR: Training and testing sets must equal 100%"
        else:
            if '-r' in flags and '-e' in flags:
                training = flags['-r']
                testing = flags['-e']
            else:
                print "ERROR: No training or testing split." + \
                    " Did you use the -r and -e flags to mark them?"

        training = float(training)/100
        testing = float(testing)/100

        ftest = open("testing_set.csv", "wb")
        ftrain = open("training_set.csv", "wb")
        wtest = csv.writer(ftest)
        wtrain = csv.writer(ftrain)

        for entry in files:
            if re.match(r".\.txt$", entry):
                f = open(location + '/' + entry, 'rb')

                if rand() < training:
                    txt_handler(f, wtrain)
                else:
                    txt_handler(f, wtest)
                f.close()
            if re.match(r".\.json$", entry):
                if len(sys.argv) > 1:
                    if json_field == "":
                        print "What key in the .json contains your text data?"
                        json_field = raw_input("Json Key: ")
                else:
                    if '-j' in flags:
                        json_fields = flags['-j']
                    if json_field == "":
                        print "Please use the -j flag to give the key of" + \
                            "the .json that contains the text data."

                f = open(location + '/' + entry, 'rb')

                if rand() < training:
                    json_handler(f, wtrain, json_field)
                else:
                    json_handler(f, wtest, json_field)
                f.close()
        ftest.close()
        ftrain.close()
    except OSError:
        print "ERROR: Directory not found"
