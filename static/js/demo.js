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

  /*global _ autocompleteTemplate headerTemplate featureTemplate issueTemplate customerServiceTemplate:true*/
  /* eslint no-console: "warn" */
'use strict';

var prodList = null;
var compareView = false;

$(document).ready(function() {

  $("#query").focus().keyup(function (e) {
    if (e.which != 13) {
      //NOT ENTER
      doAutocomplete();
    } else {
      //HIT ENTER
      console.log("ENTER");
    }
  });

  //Used just to get rid of the lint errors saying that the click functions weren't used.
  var i = true;
  if(i == false) {
    clickCompare();
    clickX({});
    clickProduct({});
  }

  $.get('/api/product-list', function(data) {
    prodList = data;
    console.log(prodList);
    $('.loader').hide();
  }).fail(function(error) {
    console.log(error);
    $('.loader').hide();
  });
});

function clickCompare() {
  var parent = $(".result--product").parent();
  $(".result--product").addClass("result--product-comparison").removeClass("result--product");
  $(".result--product--x").show();
  $(".result--compare-results").hide();
  parent.append($(".result--product-comparison").clone().addClass("pane_2"));
  $(".result--search--input").attr("placeholder", "Enter a product name to compare to");
  $(".pane_2").find(".result--product-details").css("visibility","hidden");
  //$(".pane_2").find(".result--product-details").hide();
  $(".pane_2").find(".result--placeholder").show();
  compareView = true;
}

function clickX(e) {
  var product = e.target.parentNode;
  console.log(product);
  $(product).remove();
  $(".result--product-comparison").addClass("result--product").removeClass("result--product-comparison").removeClass("pane_2");
  $(".result--product--x").hide();
  $(".result--compare-results").show();
  $(".result--search--input").attr("placeholder", "Enter a product name");
  compareView = false;
}

function clickProduct(e) {
  var productId = e.target.nextElementSibling.innerText;
  $("#query").val('');
  doAutocomplete();
  console.log(productId);
  updateProduct(productId);
}

function updateProduct(prodId) {
  $.get('/api/product?productId=' + prodId, function(data) {
    var parent = null;
    if(compareView) {
      parent = $(".pane_2");
      parent.find(".result--product-details").css("visibility","visible");
    } else {
      parent = $(".result--product");
    }

    parent.find(".result--product-details").show();
    parent.find(".result--placeholder").hide();

    console.log(data);
    fixKeywords(data);
    var maxPercent = normalizePercents(data);
    var headerTemp = headerTemplate.innerHTML;
    parent.find('.result--header').html(_.template(headerTemp, {
      item: data
    }));

    var featuresTemp = featureTemplate.innerHTML;
    parent.find('.result--features').html(_.template(featuresTemp, {
      items: data.features,
      maxPercent: maxPercent
    }));

    var issueTemp = issueTemplate.innerHTML;
    parent.find('.result--issues').html(_.template(issueTemp, {
      item: data.issues
    }));

    var customerServiceTemp = customerServiceTemplate.innerHTML;
    parent.find('.result--customer-service').html(_.template(customerServiceTemp, {
      item: data.customer_service
    }));

    if(compareView) {
      parent.find(".result--product--x").show();
      parent.find(".result--compare-results").hide();
    }

  }).fail(function(error) {
    console.log(error);
  });

}

function doAutocomplete() {
    //return "Samsung UN19F4000 19-Inch 720p 60Hz Slim LED HDTV";
    var maxLen = 3;
    var len = 0;
    var query = $("#query").val();
    var filteredProdList = [];
    if(query != "") {
      //filteredProdList = prodList.filter(function(val) {
      filteredProdList = prodList.products.filter(function(val) {
        if(len < maxLen && val.name.toUpperCase().indexOf(query.toUpperCase()) > -1) {
          len += 1;
          return val;
        }
      });
    }
    var autocompleteTemp = autocompleteTemplate.innerHTML;
    $('.result--autocomplete').html(_.template(autocompleteTemp, {
      items: filteredProdList
    }));

}

function normalizePercents(data) {
  //var maxPercent = Math.ceil(data.features[0].percentage/10)*10;
  var maxPercent = data.features[0].percentage;
  //console.log(maxPercent);
  data.features.map(function(item) {
    item.showPercentage = item.percentage/maxPercent * 100;
  });

  return maxPercent
}

function fixKeywords(data) {
  data.features.map(function(feature) {
    feature.keywords.map(function(keyword) {
      if(keyword.name.length > 10) {
        keyword.name = keyword.name.substring(0, 7) + "...";
      }
      keyword.name = keyword.name.charAt(0).toUpperCase() + keyword.name.slice(1);
    });
  });
}




/*
Tabbed Panels js
*/
(function() {
  $('.tab-panels--tab').click(function(e) {
    e.preventDefault();
    var self = $(this);
    var inputGroup = self.closest('.tab-panels');
    var idName = null;

    inputGroup.find('.active').removeClass('active');
    self.addClass('active');
    idName = self.attr('href');
    $(idName).addClass('active');
  });
})();
