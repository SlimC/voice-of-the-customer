/**
 * Created by zainadmani on 7/7/16.
 */
/**
 * Copyright 2016 IBM Corp. All Rights Reserved.
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
var debug = require('debug')('scc:cloudant-mock-data');

module.exports = function(prodId) {
    debug('WARNING: Using mock data.');

    var mockJSON = [
        { //Mock data response
            product_name: 'Samsung Galaxy S7',
            product_id: '100',
            description: 'Great phone made by Samsung that runs Android. Hundreds of features that are not available anywhere else and made by a compnay you can trust.',
            features: [
                {
                    group_name: 'Battery',
                    percentage: 80,
                    keywords: [
                        {
                            name: 'Dies fast',
                            review_ids: [264, 875]
                        },
                        {
                            name: 'Slow charging',
                            review_ids: [941, 836]
                        },
                        {
                            name: 'short',
                            review_ids: [634]
                        }
                    ],
                    sentiments: {
                        positive: 20,
                        neutral: 2,
                        negative: 78
                    }
                },
                {
                    group_name: 'Processor',
                    percentage: 12,
                    keywords: [
                        {
                            name: 'Fast',
                            review_ids: [392, 120]
                        },
                        {
                            name: 'No lag',
                            review_ids: [4, 19]
                        },
                        {
                            name: 'gaming',
                            review_ids: [749]
                        }
                    ],
                    sentiments: {
                        positive: 75,
                        neutral: 20,
                        negative: 5
                    }
                },
                {
                    group_name: 'Display',
                    percentage: 8,
                    keywords: [
                        {
                            name: 'Screen',
                            review_ids: [111, 3]
                        },
                        {
                            name: 'Color',
                            review_ids: [9193, 13, 83]
                        },
                        {
                            name: 'Resolution',
                            review_ids: [9374, 2134, 452]
                        }
                    ],
                    sentiments: {
                        positive: 81,
                        neutral: 3,
                        negative: 16
                    }
                }
            ],
            issues: {
                percentage: 10,
                review_ids: [125, 932, 10]
            },
            customer_service: {
                sentiment: {
                    positive: 24,
                    neutral: 31,
                    negative: 45
                },
                positive_sentence: "They had GREAT service!",
                neutral_sentence: "Customer Service was ok",
                negative_sentence: "They don't care about the customer at all, really need to revamp Customer Service."
            }
        },
        { //Mock data response
            product_name: 'iPhone 6s',
            product_id: '101',
            description: 'Great phone made by Apple. Quality product from a quality company.',
            features: [
                {
                    group_name: 'Screen',
                    percentage: 37,
                    keywords: [
                        {
                            name: 'fragile',
                            review_ids: [264, 875]
                        },
                        {
                            name: 'scratches easily',
                            review_ids: [941, 836]
                        },
                        {
                            name: 'smooth',
                            review_ids: [634]
                        }
                    ],
                    sentiments: {
                        positive: 15,
                        neutral: 12,
                        negative: 73
                    }
                },
                {
                    group_name: 'Processor',
                    percentage: 32,
                    keywords: [
                        {
                            name: 'Fast',
                            review_ids: [392, 120]
                        },
                        {
                            name: 'lag',
                            review_ids: [4, 19]
                        },
                        {
                            name: 'heated up',
                            review_ids: [100, 38]
                        }
                    ],
                    sentiments: {
                        positive: 35,
                        neutral: 60,
                        negative: 5
                    }
                },
                {
                    group_name: 'Display',
                    percentage: 12,
                    keywords: [
                        {
                            name: 'Viewing Angles',
                            review_ids: [111, 3]
                        },
                        {
                            name: 'Color',
                            review_ids: [9193, 13, 83]
                        },
                        {
                            name: 'Sharpness',
                            review_ids: [9374, 2134, 452]
                        }
                    ],
                    sentiments: {
                        positive: 81,
                        neutral: 3,
                        negative: 16
                    }
                }
            ],
            issues: {
                percentage: 19.281,
                review_ids: [125, 932, 10]
            },
            customer_service: {
                sentiment: {
                    positive: 30,
                    neutral: 51,
                    negative: 19
                },
                positive_sentence: "They had GREAT service!",
                neutral_sentence: "Customer Service was ok",
                negative_sentence: "They don't care about the customer at all, really need to revamp Customer Service."
            }
        }
    ];

    var result = mockJSON.filter(function(e){ return e.product_id === prodId; });
    console.log(result);
    if (result.length == 0) {
        return null;    
    } else if (result.length == 1) {
        return result[0];
    } else {
        return null;
    }
};
