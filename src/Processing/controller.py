import cloudant
import testdb
import runNLC
import clustering


DB_USERNAME = 											#Replace with your server URL
DB_PASSWORD =
DB_ACCOUNT =
DATABASE =

f = open('num.txt','rb+')
lines = f.readlines()
num = lines[-1] +
status = num[0:1]
num = num[1:]

client = Cloudant(DB_USERNAME,DB_PASSWORD,account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

raw = db.get_view_result('_design/names','review')

i = 0
n = 999
j = 0

finished = []
 if status == 'sb' or status == 'sr':
    raw = raw[num:]
    for doc in raw:

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

        if i % n == 0 or i = len(raw):
            f.write("sr%i\n" % j)
            db.bulk_docs(finished[])
            i = 0
    status = "fr"
    f.write("fr%i\n" % j)
    raw = db.get_view_result('_design/names','replaced')
    finished = []
    j = 0

if status == "fr" or status == "sc":
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        doc = runNLC.classify(doc)
        finished[i] = new_doc
        i += 1
        j += 1

        if i % n == 0 or i = len(raw):
            f.write("sc%i\n" % j)
            db.bulk_docs(finished[])
            i = 0
    status = "fc"
    f.write("fc%i\n" % j)
    raw = db.get_view_result('_design/names','classified')
    finished = []
    j = 0

#TODO finish clustering portion of the script
if status == "fc" or status == "su":
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        ident = doc['review_id']
        processed = cluster(doc)
        review = db[ident]
        asin = review['asin']
        processed['product_id'] = asin
        i += 1
        j += 1
        if i % n == 0 or i = len(raw):
            f.write("su%i\n" % j)
            db.bulk_docs(finished[])
            i = 0
    status = "fu"
    f.write("fu%i\n" % j)
    raw = db.get_view_result('_design/names','clustered')
    finished = []
    j = 0

if status == "fu" or status == "sf":
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        final = make_final(doc, db)
        final['type'] = ['final']

        if i % n == 0 or i = len(raw):
            f.write("sf%i\n" % j)
            db.bulk_docs(finished[])
            i = 0
    status = "ff"
    f.write("finished")
f.close()
