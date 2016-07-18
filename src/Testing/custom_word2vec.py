from cloudant.client import Cloudant
import gensim
import sys

DB_USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'													#Replace with your server URL
DB_PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'
DB_ACCOUNT = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
DATABASE = 'amazon_data'

class MySentences():

    def __init__(self):
        client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
        client.connect()
        global db
        db = client[DATABASE]

    def __iter__(self):
        i = 0
        for document in db:
            if i > int(sys.argv[1]):
                break
            print document
            print i
            i+=1
            if 'reviewText' in document:
                line = document['reviewText']
                yield line.split()
corpus = MySentences()
model = gensim.models.Word2Vec()
model.build_vocab(corpus)
model.save('custom_word2vec.model')
model.train(corpus)
model.save('custom_word2vec.model')
