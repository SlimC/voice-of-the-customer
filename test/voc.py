import os
import cf_deployment_tracker
import cloudant
import configparser
from flask import jsonify

def get_db():
    #getting current directory
    curdir = os.getcwd()
    try:
        #loading credentials from .env file
        cred_file_path = os.path.join(curdir, '..', '.env')
        config = configparser.ConfigParser()
        config.read(cred_file_path)
    except IOError:
        print 'warning: no .env file loaded'

    #Connect to cloudant db
    client = cloudant.client.Cloudant(config['CLOUDANT']['CLOUDANT_USERNAME'],
                                      config['CLOUDANT']['CLOUDANT_PASSWORD'],
                                      account=config['CLOUDANT']['CLOUDANT_USERNAME'])
    client.connect()
    return client[config['CLOUDANT']['CLOUDANT_DB']]

def get_product_list():
    """returns the list of products to the client for type ahead"""
    products = []
    database = get_db()
    designdocument = cloudant.design_document.DesignDocument(database, document_id="_design/names")
    docs = cloudant.view.View(designdocument, "final")
    for result in docs.result:
        try:
            doc = result['value']
            doc_entry = {}
            doc_entry['id'] = doc['_id']
            doc_entry['name'] = doc['product_name']
            products.append(doc_entry)
        except KeyError:
            print 'Error when creating list of products.'
    json_products = {"products":products}
    return jsonify(json_products)
