# Voice of the Customer [![Build Status](https://travis.innovate.ibm.com/watson-developer-cloud/product-intelligence.svg?token=ouxuNEZVg24FqsCxcPYL)](https://travis.innovate.ibm.com/watson-developer-cloud/product-intelligence)

## Installation

This is an Starter Kit (SK), which is designed to get you up and running quickly with a common industry pattern, and to provide information and best practices around Watson services. This application was created to demonstrate how the services can be used to detect sentiment and customer's satisfaction based on different product reviews. This demo for this SK uses reviews from Amazon around products from the Electronics section.

Demo: https://product-intel-demo.mybluemix.net/

**IMPORTANT:**
1. The Weather API requires an API key with high tranasctions limits. You need to upgrade to the Standard or Premimum plan. The pricing model is based on the number of calls per minute to the REST APIs. The Free and Base plans allow you to make a maximum of 10 API calls per minute. The Standard and Premimum plans allow you to make 150 and 375 API calls per minute respectively. Each plan has a maximum number of API calls allowed.  The Premimum plan is ideal. 

2. This application requires an AlchemyAPI key with high transaction limits. The free AlchemyAPI key that you request has a limit of 1000 transactions per day, which is insufficient for significant use of this sample application.  You can upgrade to the Standard or Advanced Plan of the AlchemyAPI service to obtain a key that supports > 1000 transactions per day. Go [here](https://console.ng.bluemix.net/catalog/services/alchemyapi/).

3. Running the application using the Facebook and Twilio bots will require credentials to access their services. Go to "Installing the bots" section.

4. The Conversation service requires training prior to running the application. Refer to Step 13 below.

## Table of Contents
 - [Getting Started](#getting-started)
 - [Training an entity detection model](#training)
 - [Processing the data](#processing)
 - [Running the application locally](#running-locally)
 - [Adapting/Extending the Starter Kit](#adaptingextending-the-starter-kit)
 - [Best Practices](#best-practices)
 - [Troubleshooting](#troubleshooting)
 
## Getting Started

The application is written in [Python](https://www.python.org/doc/). Instructions for downloading and installing it are included in the documentation.

1. Log into GitHub and fork the project repository. Clone your fork to a folder on your local system and change to that folder.
2. Create a Bluemix Account. [Sign up][sign_up] in Bluemix, or use an existing account. Watson Beta or Experimental Services are free to use.
3. If it is not already installed on your system, download and install the [Cloud-foundry CLI][cloud_foundry] tool.
4. Edit the `manifest.yml` file in the folder that contains your fork and replace `application-name` with a unique name for your copy of the application. The name that you specify determines the application's URL, such as `application-name.mybluemix.net`. The relevant portion of the `manifest.yml` file looks like the following:

      ```yaml
      declared-services:
  		natural-language-classifier-service:
    	  label: natural_language_classifier
    	  plan: standard
        cloudantNoSQLDB-service:
          label: cloudantNoSQLDB
          plan: Shared
      applications:
      - services:
         - natural-language-classifier-service
         - cloudantNoSQLDB-service
        name: product-intel-demo
        command: python server.py
        path: .
        memory: 512M
      ```

5. Install the python dependencies with `pip`

    ```sh
    pip install -r requirements.txt
    ```

6. Connect to Bluemix by running the following commands in a terminal window:

    ```bash
    cf api https://api.ng.bluemix.net
    cf login -u <your-Bluemix-ID> -p <your-Bluemix-password>
    ```
    
7. Create and retrieve service keys to access the [Natural Language Classifier][natural-language-classifier] service by running the following commands:
  ```
  cf create-service natural_language_classifier standard natural-language-classifier-service
  cf service-key natural-language-classifier-service myKey
  ```
  **Note:** You will see a message that states "Attention: The plan standard of `service natural_language_classifier` is not free. The instance classifier-service will incur a cost. Contact your administrator if you think this is in error.". The first Natural Language Classifier instance that you create is free under the standard plan, so there will be no change if you only create a single classifier instance for use by this application.


8. Create and retrieve service keys for the Alchemy Language service. If you are using an existing alchemy service, use those credentials instead.

    ```bash
    cf create-service-key alchemy-language-service myKey
    cf service-key alchemy-language-service myKey
    ```

9. Create and retrieve service keys for the Cloudant service. If you are using an existing alchemy service, use those credentials instead.

    ```bash
    cf create-service-key cloudantNoSQLDB-service myKey
    cf service-key cloudantNoSQLDB-service myKey
    ```

10. Provide the credentials to the application by creating a `.env` file using this format: (**Note**: there is an example .env.example file in the root directory of your forked code instance)

    ```none
    source venv/bin/activate
    
    ALCHEMY_API_KEY=
	VARIABLE_NAME=
	
    #NLC
    NLC_URL=https://gateway.watsonplatform.net/conversation/api
    NLC_USERNAME=
    NLC_PASSWORD=

    #CLOUDANT
    CLOUDANT_URL=
    CLOUDANT_USERNAME=
    CLOUDANT_PASSWORD=
    CLOUDANT_DB=
    ```

11. The Natural Language Classifier requires training prior to using the application. The training data is provided in `resources/classifier-training-data.csv`. Adapt the following curl command to train your classifier (replace the username and password with the service credentials of the Natural Language Classifier created in the last step):
```
curl -u "{username}":"{password}" -F training_data=@resources/classifier-training-data.csv -F training_metadata="{\"language\":\"en\",\"name\":\"My Classifier\"}" "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"
```

12. Push the updated application live by running the following command:

    ```bash
    cf push
    ```
    or by pressing the "Deploy to Bluemix" button below.

    [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/watson-developer-cloud/product-intelligence.git)

## Training an entity detection model 

The Training phase is responsible for creating a customized model which detects entities related to the topic of the reviews. This model can be created by using Watson Knowledge Studio (WKS) for annotating the data (product reviews) to detect entities and their relationships.

The WKS tool exports an Alchemy customized model that is then able to extract entities and relationships from unseen data. The steps to preprocess the data and create the models are detailed in the iPython notebooks under the `notebooks` folder of this repo.

1. Getting the data
2. Training the WKS Model
3. Making training/testing sets
4. Doing entity replacement on the training/testing sets
5. Designing the NLC tree
6. Doing the hand classification on the replaced training and testing set
7. Training the classifiers

## Processing the data (What the src/Processing/controller.py does)

1. Take review and run it through entity extraction
2. Run it through classifier
3. Cluster
4. make Final JSON actually turns this into something a front end can use

## Adapting/Extending the Starter Kit

<a>
# Architecture Diagram
</a>

![](readme_images/VoC-ArchitectureFlow.jpg)

This Starter Kit works off of product reviews data gathered from Amazon product reviews (http://jmcauley.ucsd.edu/data/amazon/). However, the concepts used here are platform independent and can be applied to a use case other than Electronic products reviews. Just define your use case and make sure you train your Natural Language Classifier accordingly by using the tool provided on the service page. Additionally, you can also create your own customized models for entity extraction by using Watson Knowledge Studio and Alchemy.

## Reference information

The following links provide more information about the Natural Language Classifier, Cloudant, and Alchemy Language services.

### Natural Language Classifier service
  * [API documentation](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/nl-classifier/): Get an in-depth knowledge of the Natural Language Classifier service
  * [API reference](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/natural-language-classifier/api/v1/): SDK code examples and reference
  * [API Explorer](https://watson-api-explorer.mybluemix.net/apis/natural-language-classifier-v1): Try out the API
  * [Creating your own classifier](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/nl-classifier/get_start.shtml): How to use the API to create and use your own classifier

### Cloudant service
  * [API documentation](https://console.ng.bluemix.net/docs/services/Cloudant/index.html#Cloudant): Get an in-depth understanding of the Cloudant services
  * [API reference](https://docs.cloudant.com/api.html#-api-reference): Code examples and reference
  
### AlchemyAPI
  * [API documentation](http://www.alchemyapi.com/api): Get an in-depth understanding of the AlchemyAPI services
  * [AlchemyData News reference](http://docs.alchemyapi.com/): API and query gallery

## Best Practices

### Intents for the NLC service instance
  * When defining intents, follow naming conventions to create consistent intents.
  * Use "-" to separate multiple levels (Example : location-weather-forecast)
  * Use "_" to separate multiple word intents (Example : business_center)
  * Provide more variations of input via examples for each intent. The more variations the better.
  * Avoid overlapping intents across examples. (Example : benefits_eligibility and benefits_elgibility_employee). To avoid this, group examples into a single intent and use entities to deal with subtle variations.
  * Examples for intents should be representative of end user input

## Troubleshooting

To troubleshoot your Bluemix application, use the logs. To see the logs, run:

  ```bash
  cf logs <application-name> --recent
  ```

## License

  This sample code is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).

## Contributing

  See [CONTRIBUTING](CONTRIBUTING.md).

## Open Source @ IBM

  Find more open source projects on the [IBM Github Page](http://ibm.github.io/)

### Privacy Notice

This node sample web application includes code to track deployments to Bluemix and other Cloud Foundry platforms. The following information is sent to a Deployment Tracker service on each deployment:

* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris`)

This data is collected from the `VCAP_APPLICATION` environment variable in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

### Disabling Deployment Tracking

Deployment tracking can be disabled by removing `require('cf-deployment-tracker-client').track();` from the beginning of the `server.py` file at the root of this repo.

### Privacy Notice

This sample web application includes code to track deployments to Bluemix and other Cloud Foundry platforms. The following information is sent to a [Deployment Tracker][deploy_track_url] service on each deployment:

* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris`)

This data is collected from the `VCAP_APPLICATION` environment variable in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

[deploy_track_url]: https://github.com/cloudant-labs/deployment-tracker
[cloud_foundry]: https://github.com/cloudfoundry/cli
[sign_up]: https://console.ng.bluemix.net/registration/
[get-alchemyapi-key]: https://console.ng.bluemix.net/catalog/services/alchemyapi/

[natural-language-classifier]: http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/nl-classifier.html
[alchemy-language]: http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/alchemy-language.html
[cloudantNoSQLDB]: https://console.ng.bluemix.net/docs/services/Cloudant/index.html#Cloudant