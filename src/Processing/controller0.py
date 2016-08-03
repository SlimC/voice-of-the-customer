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
skipped = []
client = cloudant.client.Cloudant(DB_USERNAME, DB_PASSWORD, account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]

if status == 'sb' or status == 'sr':
    raw = db.get_view_result('_design/names', 'review')
    i = 0
    n = 999
    j = 0
    finished = [0]*1000
    raw = raw[num:]
    for doc in raw:
        new_doc = {}
        doc = doc['value']
        asin = doc['asin']
        query = cloudant.query.Query(db, selector={'product_id': asin, 'type': ['final']})
        if query.result[0] == []:
            review_id = doc['_id']
            new_doc['review_id'] = review_id
            text = doc['reviewText']
            text = token_replacement.token_replacement(text)
            new_doc['review'] = text
            new_doc['type'] = ['replaced']
            j += 1
            db.create_document(new_doc)
            f.write("sr%i\n" % j)
    status = "fr"
    f.write("fr0\n")
    num = 0

if status == "fr" or status == "sc":
    raw = db.get_view_result('_design/names', 'replaced')
    finished = [0] * 1000
    j = 0
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        rev_id = doc['review_id']
        query = cloudant.query.Query(db, selector={'review_id': rev_id, 'type': ['final']})
        if query.result[0] == []:
            del doc['_id']
            new_doc = runNLC.classify(doc)
            print new_doc
            db.create_document(new_doc)
            j += 1
            f.write("sc%i\n" % j)
    status = "fc"
    f.write("fc0\n")
    num = 0

# TODO finish clustering portion of the script
if status == "fc" or status == "su":
    raw = db.get_view_result('_design/names', 'classified')
    finished = [0] * 1000
    j = 0
    raw = raw[num:]
    processed_asin = []
    for doc in raw:
        doc = doc['value']
        rev_id = doc['review_id']
        query = cloudant.query.Query(db, selector={'review_id': rev_id, 'type': ['clustered']})
        if query.result[0] == []:
            del doc['_id']
            ident = doc['review_id']
            review = db[ident]
            asin = review['asin']
            if asin not in processed_asin:
                processed = clustering.cluster(doc, db, asin)
                processed_asin.append(asin)
                processed['product_id'] = asin
                processed['type'] = ['clustered']
                j += 1
                db.create_document(processed)
                f.write("su%i\n" % j)
                i = 0
    status = "fu"
    f.write("fu0\n")
    num = 0

if status == "fu" or status == "sf":
    raw = db.get_view_result('_design/names', 'clustered')
    finished = [0] * 1000
    j = 0
    raw = raw[num:]
    for doc in raw:
        doc = doc['value']
        name = doc['product_name']
        asin = doc['product_id']
        query = cloudant.query.Query(db, selector={'product_id': asin, 'type': ['final']})
        if query.result[0] == []:
            del doc['_id']
            final = {}
            final = makeFinalJSON.make_final(doc, db)
            final['type'] = ['final']
            final['product_id'] = asin
            final['product_name'] = name
            j += 1
            db.create_document(final)
            f.write("sf%i\n" % j)
    status = "ff"
    f.write("finished")
f.close()
