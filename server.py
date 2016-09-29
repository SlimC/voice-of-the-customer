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
from cloudant.client import Cloudant
from requests.exceptions import HTTPError
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

try:
    load_dotenv(find_dotenv())
except Exception:
    print 'warning: no .env file loaded'

# Emit Bluemix deployment event
cf_deployment_tracker.track()

#Connect to cloudant db
dbClient = Cloudant(os.environ['CLOUDANT_USER'], os.environ['CLOUDANT_PW'], url=os.environ['CLOUDANT_URL'])
dbClient.connect()
cloundantDB = dbClient[os.environ['CLOUDANT_DB']]

# Application routes

@app.route('/', methods=['GET'])
def index():
    """returns the html to the client"""
    return render_template('index.html')

#Temporary for until I change this to load from cloudant, a file, or something less ugly
@app.route('/api/product-list', methods=['GET'])
def get_product_list():
    """returns a list of known products to the client for type ahead"""
    return jsonify([{"id":"22e6343bf6748a6c408fac1e0c69f3c3", "name":"Microsoft Comfort Mouse 4500 - Poppy Red"},
                    {"id":"56644a772c2ec9e89f6ce785b1c1528e", "name": "Microsoft Comfort Mouse 4500"},
                    {"id":"6666526730953249e153fb108eee5fa1", "name" : "Garmin n&uuml;vi 65LM GPS Navigators System with Spoken Turn-By-Turn Directions, Preloaded Maps and Speed Limit Displays (Lower 49 U.S. States)"},
                    {"id":"9dcef3aea4f4827c8d26dd834387f73a", "name":"Bose QuietComfort 15 Acoustic Noise Cancelling Headphones"},
                    {"id":"f9204a0a8eaf8e5e7c4cb935138f8f4c", "name":"Kidz Gear Wired Headphones For Kids - Gray"},
                    {"id":"9dcef3aea4f4827c8d26dd8343bace76", "name":"Seiki SE22FR01 22-Inch 1080p 60Hz LED HDTV"},
                    {"id":"c8b860c1d45364dde8e127959a86733b", "name":"Samsung UN19F4000 19-Inch 720p 60Hz Slim LED HDTV"},
                    {"id":"c8b860c1d45364dde8e127959a9ec566", "name":"Garmin n&uuml;vi 55LMT GPS Navigators System with Spoken Turn-By-Turn Directions, Preloaded Maps and Speed Limit Displays (Lower 49 U.S. States)"},
                    {"id":"d045f1b39d53302d09ed5a5e4d82c5a0", "name":"VIZIO M651d-A2R 65-Inch 1080p 240Hz 3D Smart LED HDTV (2013 Model)"},
                    {"id":"100", "name" : "Samsung Galaxy S7"},
                    {"id":"101", "name" : "iPhone 6s"}])

@app.route('/api/product', methods=['GET'])
def get_product():
    """retrieves data on a product from the cloudant db and sends to client"""
    print request.args.get('productId')
    return jsonify(cloundantDB[request.args.get('productId')])

@app.errorhandler(Exception)
def handle_error(err):
    """Catces errors with processing client requests and returns message"""
    code = 500
    error = 'Error processing the request'
    app.logger.error('Exception : %r' % err)
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
