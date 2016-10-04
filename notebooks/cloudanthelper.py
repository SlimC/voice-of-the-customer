import configparser
import os
from cloudant.client import Cloudant
from cloudant import design_document
from cloudant import view
from cloudant import document

#getting current directory
CURDIR = os.getcwd()

try:
    #loading credentials from .env file
    CREDFILEPATH = os.path.join(CURDIR, '.env')
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CREDFILEPATH)
except:
    print 'warning: no .env file loaded'

CLOUDANT_USERNAME = config['CLOUDANT']['CLOUDANT_USERNAME']
CLOUDANT_PASSWORD = config['CLOUDANT']['CLOUDANT_PASSWORD']
ACCOUNT_NAME = config['CLOUDANT']['CLOUDANT_USERNAME']

def getConnection():
    my_client = Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, account=ACCOUNT_NAME)
    my_client.connect()
    my_session = my_client.session()
    if my_session is None:
        print "Connection unsuccessful"
    return my_client

def convertToDocument(database, doc_id):
    return document.Document(database, document_id=doc_id)

def getResultsfromView(view_name, design_document_name, database):
    design_document = design_document.DesignDocument\
    (database, document_id=design_document_name)
    my_view = view.View(design_document, view_name)
    return my_view

def createView(database, view_name, map_func):
    design_document = design_document.DesignDocument(database, "_design/names")
    design_document.add_view(view_name, map_func)
    return view.View(design_document, view_name, map_func)

def create_tracker(database):
    # Creating document to track status of reviews
    model_tracker = { \
                    '_id': 'tracker', \
                    'cluster_switch': 0, \
                    'classify_switch': 0, \
                    'replace_switch': 0, \
                    'final_switch': 0, \
                    'finished_switch': 0, \
                    'replaced': [], \
                    'classified': [], \
                    'clustered': [], \
                    'final': [] \
                    }

    status = {}
    try:
        status = database['tracker']
    except KeyError:
        status = database.create_document(model_tracker)
