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

import os
import configparser
from cloudant.client import Cloudant
from cloudant import design_document
from cloudant import view
from cloudant import document

#getting current directory
CURDIR = os.getcwd()

try:
    #loading credentials from .env file
    CRED_FILE_PATH = os.path.join(CURDIR, '..', '.env')
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CRED_FILE_PATH)
except IOError:
    print 'warning: no .env file loaded'

CLOUDANT_USERNAME = CONFIG['CLOUDANT']['CLOUDANT_USERNAME']
CLOUDANT_PASSWORD = CONFIG['CLOUDANT']['CLOUDANT_PASSWORD']
ACCOUNT_NAME = CONFIG['CLOUDANT']['CLOUDANT_USERNAME']

def getConnection():
    """
    Creates and returns a Cloudant connection.
    """
    my_client = Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, account=ACCOUNT_NAME)
    my_client.connect()
    my_session = my_client.session()
    if my_session is None:
        print "Connection unsuccessful"
    return my_client

def convertToDocument(database, doc_id):
    """
    Converts a json object into a Cloudant Document object.
    """
    return document.Document(database, document_id=doc_id)

def getResultsfromView(view_name, design_document_name, database):
    """
    Returns documents based on a Cloudant View.
    """
    my_design_document = design_document.DesignDocument\
    (database, document_id=design_document_name)
    my_view = view.View(my_design_document, view_name)
    return my_view

def createView(database, view_name, map_func):
    """
    Creates and returns a Cloudant view.
    """
    my_design_document = design_document.DesignDocument(database, "_design/names")
    my_design_document.add_view(view_name, map_func)
    return view.View(my_design_document, view_name, map_func)

def create_tracker(database):
    """
    Creates a tracker document in Cloudant to track phase status.
    """
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

    try:
        status = database['tracker']
    except KeyError:
        status = database.create_document(model_tracker)
