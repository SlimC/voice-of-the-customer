import cloudant
import runNLC
import clustering
import token_replacement
import makeFinalJSON


def add_review(status):
    cluster = status['cluster_switch']
    classify = status['classify_switch']
    replace = status['replace_switch']
    review = status['review_switch']
    final = status['final_switch']
    finished = status['finished_switch']
    num = cluster + classify + replace + review + final + finished
    return num

DB_USERNAME = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
DB_PASSWORD = '5beb3f8b9f95586542e3d9c5acfb0c52832252432623e534d4e88b12fad29638'
DB_ACCOUNT = '1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix'
DATABASE = 'testdb'

model_tracker = {
                    '_id': 'tracker',
                    'cluster_switch': 0,
                    'classify_switch': 0,
                    'replace_switch': 0,
                    'review_switch': 1,
                    'final_switch': 0,
                    'finished_switch': 0,
                    'replaced': [],
                    'classified': [],
                    'clustered': [],
                    'final': []
                }

client = cloudant.client.Cloudant(DB_USERNAME, DB_PASSWORD, account=DB_ACCOUNT)
client.connect()
db = client[DATABASE]
status = {}

try:
    status = db['tracker']
except KeyError:
    status = db.create_document(model_tracker)

if add_review(status) < 3:
    status['replace_switch'] = 1
    status.save()
    raw = db.get_view_result('_design/names', 'review')
    for doc in raw:
        new_doc = {}
        doc = doc['value']
        asin = doc['asin']
        if doc['_id'] not in status['replaced']:
            review_id = doc['_id']
            new_doc['review_id'] = review_id
            text = doc['reviewText']
            text = token_replacement.token_replacement(text)
            new_doc['review'] = text
            new_doc['type'] = ['replaced']
            new_doc['asin'] = asin
            status['replaced'].append(review_id)
            db.create_document(new_doc)
            status.save()
    status['classify_switch'] = 1
    status.save()

if add_review(status) == 3:
    raw = db.get_view_result('_design/names', 'replaced')
    for doc in raw:
        doc = doc['value']
        rev_id = doc['review_id']
        if rev_id not in status['classified']:
            doc_id = doc['_id']
            del doc['_id']
            new_doc = runNLC.classify(doc)
            status['classified'].append(doc_id)
            db.create_document(new_doc)
            status.save()
    status['cluster_switch'] = 1

if add_review(status) == 4:
    raw = db.get_view_result('_design/names', 'classified')
    for doc in raw:
        doc = doc['value']
        rev_id = doc['review_id']
        del doc['_id']
        review = db[rev_id]
        asin = review['asin']
        if asin not in status['clustered']:
            processed = clustering.cluster(doc, db, asin)
            processed['product_id'] = asin
            processed['type'] = ['clustered']
            status['clustered'].append(asin)
            db.create_document(processed)
            status.save()
    status['final_switch'] = 1

if add_review(status) == 5:
    raw = db.get_view_result('_design/names', 'clustered')
    for doc in raw:
        doc = doc['value']
        name = doc['product_name']
        asin = doc['product_id']
        if asin not in status['finished']:
            del doc['_id']
            final = {}
            final = makeFinalJSON.make_final(doc, db)
            final['type'] = ['final']
            final['product_id'] = asin
            final['product_name'] = name
            status['finished'].append(asin)
            db.create_document(final)
            status.save()
    status['finished_switch'] = 1
    status.save()

if add_review(status) > 5:
    print 'Finished'
