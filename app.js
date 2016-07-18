/**
 * Copyright 2015 IBM Corp. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/* eslint no-unused-vars: "warn" */
'use strict';

var express = require('express');
var app = express();
//var watson = require('watson-developer-cloud');
var cloudant = require('cloudant');

// if bluemix credentials exists, then override local
var mockUp = true;
var credentials = {
	key: 'ngeryfornewareseveryseen',
	password: 'e75a6f3000ad59bde1cc03115335ac2b0b091b5c',
	url: 'https://ngeryfornewareseveryseen:e75a6f3000ad59bde1cc03115335ac2b0b091b5c@1790ef54-fcf2-4029-9b73-9000dff88e6e-bluemix.cloudant.com',
	version: 'v1'
};

// Bootstrap application settings
require('./config/express')(app);

// <service name> is coming from node_modules/watson-developer-cloud/lib/index.js
app.get('/', function(req, res) {
	res.render('index');
});

app.get('/api/product', function(req, res) {
	if(!req.query.productId) {
		return "";
	}

	if(mockUp) {
		//load mock data json from cloundant-mock-data.js
		var mockData = require('./data/cloudant-mock-data')();
		return res.json(mockData);
	} else {
		cloudant(credentials.url, function(err/*, cloud*/) {
			if (err) {
				return 'Failed to initialize Cloudant: ' + err.message;
			} else {
				return 'Connected successfully to Cloudant';
			}
		});
	}
});

// error-handler application settings
require('./config/error-handler')(app);

module.exports = app;
