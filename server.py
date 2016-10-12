#!/usr/bin/env python
#
# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -*- coding: utf-8 -*-

"""
    usage: python server.py
    description: Run the Flask web server
"""
import os
import cf_deployment_tracker
import cloudant
import configparser
from requests.exceptions import HTTPError
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

#getting current directory
CURDIR = os.getcwd()

try:
    #loading credentials from .env file
    CREDFILEPATH = os.path.join(CURDIR, '.env')
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CREDFILEPATH)
except IOError:
    print 'warning: no .env file loaded'

#Connect to cloudant db
CLIENT = cloudant.client.Cloudant(CONFIG['CLOUDANT']['CLOUDANT_USERNAME'],
                                  CONFIG['CLOUDANT']['CLOUDANT_PASSWORD'],
                                  account=CONFIG['CLOUDANT']['CLOUDANT_USERNAME'])
CLIENT.connect()

REVIEWS_DB = CLIENT[CONFIG['CLOUDANT']['CLOUDANT_DB']]

# Emit Bluemix deployment event
cf_deployment_tracker.track()

# Application routes
@app.route('/', methods=['GET'])
def index():
    """returns the html to the client"""
    return render_template('index.html')

@app.route('/api/product-list', methods=['GET'])
def get_product_list():
    """returns the list of products to the client for type ahead"""
    products = []
    designdocument = cloudant.design_document.DesignDocument(REVIEWS_DB, document_id="_design/names")
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

@app.route('/api/product', methods=['GET'])
def get_product():
    """retrieves data on a product from the cloudant db and sends to client"""
    print request.args.get('productId')
    return jsonify(REVIEWS_DB[request.args.get('productId')])

@app.errorhandler(Exception)
def handle_error(err):
    """Catches errors with processing client requests and returns message"""
    code = 500
    error = 'Error processing the request'
    if isinstance(err, HTTPError):
        code = err.code
        error = str(err.message)

    return jsonify(error=error, code=code), code

if __name__ == "__main__":
    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv('VCAP_APP_HOST', '127.0.0.1')
    PORT_NUMBER = int(os.getenv('VCAP_APP_PORT', '3000'))

    # Start the server
    app.run(host=HOST_NAME, port=PORT_NUMBER, debug=True)
    print 'Listening on %s:%d' % (HOST_NAME, PORT_NUMBER)
