import configparser
import os
from cloudant.client import Cloudant
from cloudant import design_document
from cloudant import view
from cloudant import document

#getting current directory
curdir = os.getcwd()

#loading credentials from .env file
credFilePath = os.path.join(curdir,'..','.env')
config = configparser.ConfigParser()
config.read(credFilePath)

CLOUDANT_USERNAME = config['CLOUDANT']['CLOUDANT_USERNAME']
CLOUDANT_PASSWORD = config['CLOUDANT']['CLOUDANT_PASSWORD']
ACCOUNT_NAME = config['CLOUDANT']['CLOUDANT_USERNAME']

def getConnection():
    client = Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, account=ACCOUNT_NAME)
    client.connect()
    session = client.session()
    if session is None:
        print "Connection unsuccessful"
    return client

def convertToDocument(db, docId):
    return document.Document(db, document_id=docId)

def getResultsfromView(viewName, designDocumentName, db):
    designdocument = design_document.DesignDocument(db,document_id=designDocumentName)
    v = view.View(designdocument, viewName)
    return v

def createView(db, viewName, mapFunc):
    designDocument = design_document.DesignDocument(db, "_design/names")
    designDocument.add_view(viewName, mapFunc)
    return view.View(designDocument, viewName, mapFunc)

def create_tracker(db):
    # Creating document to track status of reviews
    model_tracker = {
                    '_id': 'tracker',
                    'cluster_switch': 0,
                    'classify_switch': 0,
                    'replace_switch': 0,
                    'final_switch': 0,
                    'finished_switch': 0,
                    'replaced': [],
                    'classified': [],
                    'clustered': [],
                    'final': []
                    }

    status = {}
    try:
        status = db['tracker']
    except KeyError:
        status = db.create_document(model_tracker)
        
if __name__ == "__main__":
    client = getConnection()
    getResultsfromView("final", "names")
    session = client.session()
    session
