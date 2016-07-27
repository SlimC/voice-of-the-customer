import cloudant
import runNLC
import clustering
import token_replacement
import makeFinalJSON


DB_USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
DB_PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'
DB_ACCOUNT = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
DATABASE = 'testdb'

f = open('num.txt', 'rb+')
lines = f.readlines()
num = lines[-1]
status = num[0:2]
print status
num = int(num[2:])
print num

client = cloudant.client.Cloudant(DB_USERNAME, DB_PASSWORD, account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

raw = db.get_view_result('_design/names', 'review')

i = 0
n = 999
j = 0

finished = [0]*1000
if status == 'sb' or status == 'sr':
    raw = raw[num:]
    for doc in raw:
        new_doc = {}
        doc = doc['value']
        review_id = doc['_id']
        new_doc['review_id'] = review_id
        text = doc['reviewText']
        text = token_replacement.token_replacement(text)
        new_doc['review'] = text
        new_doc['type'] = ['replaced']
        finished[i] = new_doc
        i += 1
        j += 1

        if i % n == 0 or i == len(raw):
            for k in range(0,i):
                db.create_document(finished[k])
            f.write("sr%i\n" % j)
            i = 0
    status = "fr"
    f.write("fr0\n")

raw = db.get_view_result('_design/names', 'replaced')
finished = [0] * 1000
j = 0
num = 0

if status == "fr" or status == "sc":
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        del doc['_id']
        new_doc = runNLC.classify(doc)
        finished[i] = new_doc
        i += 1
        j += 1
        if i % n == 0 or i == len(raw):
            for k in range(0, i):
                db.create_document(finished[k])
            f.write("sc%i\n" % j)
            i = 0
    status = "fc"
    f.write("fc0\n")
raw = db.get_view_result('_design/names', 'classified')
finished = [0] * 1000
j = 0
num = 0

# TODO finish clustering portion of the script
if status == "fc" or status == "su":
    raw = raw[num:]
    processed = []
    for doc in raw:
        doc = doc['value']
        ident = doc['review_id']
        del doc['_id']
        review = db[ident]
        asin = review['asin']
        if asin not in processed:
            processed = clustering.cluster(doc, db, asin)
            processed['product_id'] = asin
            processed['type'] = ['clustered']
            finished[i] = processed
            processed.append(asin)
            i += 1
            j += 1
        if i % n == 0 or i == len(raw):
            for k in range(0, i):
                db.create_document(finished[k])
            f.write("su%i\n" % j)
            i = 0
    status = "fu"
    f.write("fu0\n")
raw = db.get_view_result('_design/names', 'clustered')
finished = [0] * 1000
j = 0
num = 0

if status == "fu" or status == "sf":
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        del doc['_id']
        final = makeFinalJSON.make_final(doc, db)
        final['type'] = ['final']
        i += 1

        if i % n == 0 or i == len(raw):
            for k in range(0, i):
                db.create_document(finished[k])
            f.write("sf0\n")
            i = 0
    status = "ff"
    f.write("finished")
f.close()
