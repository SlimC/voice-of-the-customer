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

  /*global _ headerTemplate featureTemplate issueTemplate customerServiceTemplate:true*/
  /* eslint no-console: "warn" */
'use strict';

$(document).ready(function() {
  $.get('/api/product?productId=' + 100, function(data) {
    console.log(data);
    var maxPercent = normalizePercents(data);
    var headerTemp = headerTemplate.innerHTML;
    $('.result--header').append(_.template(headerTemp, {
      item: data
    }));

    var featuresTemp = featureTemplate.innerHTML;
    $('.result--features').append(_.template(featuresTemp, {
      items: data.features,
      maxPercent: maxPercent
    }));

    var issueTemp = issueTemplate.innerHTML;
    $('.result--issues').append(_.template(issueTemp, {
      item: data.issues
    }));

    var customerServiceTemp = customerServiceTemplate.innerHTML;
    $('.result--customer-service').append(_.template(customerServiceTemp, {
      item: data.customer_service
    }));

    $('.loader').hide();

  }).fail(function(error) {
    console.log(error);
  });
});

function normalizePercents(data) {
  //var maxPercent = Math.ceil(data.features[0].percentage/10)*10;
  var maxPercent = data.features[0].percentage;
  //console.log(maxPercent);
  data.features.map(function(item) {
    item.showPercentage = item.percentage/maxPercent * 100;
  });

  return maxPercent
}




