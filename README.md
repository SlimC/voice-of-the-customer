# Voice of the Customer [![Build Status](https://travis-ci.org/watson-developer-cloud/voice-of-the-customer.svg?branch=master)](https://travis-ci.org/watson-developer-cloud/voice-of-the-customer/)

This is a Starter Kit (SK), which is designed to get you up and running quickly with a common industry pattern, and to provide information and best practices around Watson services. This application was created to demonstrate how the services can be used to detect sentiment and customer's satisfaction based on different product reviews. This demo for this SK uses reviews of electronics products on Amazon.

**IMPORTANT NOTES:**
1. You must sign up to use the Watson Knowledge Studio tool. A 30-day free trial is available. Go to the [WKS](https://www.ibm.com/marketplace/cloud/supervised-machine-learning/us/en-us) link to learn more.

2. The application requires an AlchemyAPI key with high transaction limits. The free AlchemyAPI key that you request has a limit of 1000 transactions per day, which is insufficient for significant use of this sample application.  You can upgrade to the Standard or Advanced Plan of the AlchemyAPI service to obtain a key that supports more than 1000 transactions per day. Go [here](https://console.ng.bluemix.net/catalog/services/alchemyapi/).

3. The Natural Language Classifier service requires training prior to running the application. Refer to the `Training` notebook in `/notebooks`.

## Table of Contents
 - [How this app works](#how-this-app-works)
 - [Getting Started](#getting-started)
 - [Installation](#installation)
 - [Running locally](#running-locally)
 - [Running the notebooks](#running-notebooks)
    - [Training an entity detection model](#training)
    - [Processing the data](#processing)
 - [Adapting/Extending the Starter Kit](#adaptingextending-the-starter-kit)
 - [Deploying the application to Bluemix](#deploying)
 - [Best Practices](#best-practices)
 - [Troubleshooting](#troubleshooting)
 - [Reference information](#ref)

## <a name="how-this-app-works"></a>How this app works
This starter kit uses Jupyter Notebook, a web application that enables you to create and share documents that contain code, visualizations, and explanatory text. (Jupyter Notebook was formerly known as iPython Notebook.) Jupyter Notebook automatically executes specific sections of Python code that are embedded in a notebook, displaying the results of those commands in a highlighted section below each block code block. The Jupyter notebooks in this SK show you how to creating an entity model, classifying and clustering the data.

This SK has 2 primary Jupyter notebooks:
   * `Training`, which shows how to take a data set, import it into Cloudant, create Ground Truth, and use WKS to create an entity model, and then train a classifier.
   * `WKS`, which runs on all of the review data after all of the models are  trained and validated.


## <a name="getting-started"></a>Getting Started

The application is written in [Python](https://www.python.org/doc/). Instructions for downloading and installing it are included in the documentation.

### Prerequisites

You need the following to use this SK:
* A UNIX-based OS (or Cygwin)
* Git
* Python 2.7.x (**Note**: Python 3.x is not supported for this SK)
* Anaconda&mdash;installing this package also installs the Jupyter notebook package, which includes iPython (now referred to as Jupyter)
* A Bluemix account

## <a name="installation"></a>Installation
1. Log into GitHub and fork the project repository. Clone your fork to a folder on your local system and change to that folder.
2. Create a Bluemix Account. [Sign up][sign_up] in Bluemix, or use an existing account. Watson Beta and Experimental Services are free to use.
3. If it is not already installed on your system, download and install the [Cloud Foundry CLI][cloud_foundry] tool.
4. Edit the `manifest.yml` file in the folder that contains your fork and, under `applications:`, replace the value of `- name:` with a unique name for your copy of the application. The name that you specify determines the application's URL, such as `application-name.mybluemix.net`. The relevant portion of the `manifest.yml` file looks like the following:

    ```yaml
    declared-services:
      alchemy-language-service:
        label: alchemy
        plan: free
      natural-language-classifier-service:
        label: natural_language_classifier
        plan: standard
      cloudantNoSQLDB-service:
        label: cloudantNoSQLDB
        plan: Free
    applications:
    - services:
       - alchemy-service
       - natural-language-classifier-service
       - cloudantNoSQLDB-service
    - name: product-intel-demo
      command: python server.py
      path: .
      memory: 512M
    ```

5. Install the python dependencies by using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

6. Connect to Bluemix by running the following commands in a terminal window:

    ```bash
    cf api https://api.ng.bluemix.net
    cf login -u <your-Bluemix-ID> -p <your-Bluemix-password>
    ```

7. Create instances of the services that are used by the application. Create and retrieve service keys to access the [Natural Language Classifier][natural-language-classifier] service by running the following commands:
  ```bash
  cf create-service-key natural-language-classifier-service <your-NLC-key>
  cf create-service-key natural_language_classifier <your-NLC-key>
  cf service-key natural-language-classifier-service <your-NLC-key>
  ```
  In this command, `<your-NLC-key>` is the credentials file found on the `natural-language-classifier-service` tile on your Bluemix Dashboard. Unless you have credentials for other services already defined, the default name for `<your-NLC-key>` is `Credentials-1`.

  **Note:** The commands return a message that states "Attention: The plan standard of `service natural_language_classifier` is not free. The instance classifier-service will incur a cost. Contact your administrator if you think this is in error." The first Natural Language Classifier instance that you create is free under the standard plan, so there is no charge if you create only a single classifier instance for use by this application.


8. Create and retrieve service keys for the Alchemy Language service. If you already have an instance of the Alchemy Language Service, you can use that instance and its API key.

    ```bash
    cf create-service alchemy-language standard alchemy-language-service
    cf create-service-key alchemy-language-service <your-AlchemyAPI-key>
    cf service-key alchemy-language-service <your-AlchemyAPI-key>
    ```

9. Create and retrieve service keys for the Cloudant service. If you are using an existing Cloudant service, use those credentials instead.

    ```bash
    cf create-service cloudantNoSQLDB standard cloudantNoSQLDB-service
    cf create-service-key cloudantNoSQLDB-service <your-Cloudant-key>
    cf service-key cloudantNoSQLDB-service <your-Cloudant-key>
    ```
**Note:** The commands return a message that warns you that the Shared plan for the Cloudant NoSQLDB service is not free.

10. A file named `.env` file is used to list the service keys for your service instances to the application. Create a `.env` file in the root directory of your clone of the project repository by copying the sample `.env.example` file by using the following command:

	```bash
	cp .env.example .env
	```
	Edit the `.env` file to add values for the listed environment variables:

    ```none
	[CLOUDANT]
	CLOUDANT_USERNAME=
	CLOUDANT_PASSWORD=
	CLOUDANT_URL=
	CLOUDANT_DB=voc_ask_db

	[NLC]
	NLC_URL=https://gateway.watsonplatform.net/natural-language-classifier/api
	NLC_USERNAME=
	NLC_PASSWORD=
	NLC_CLASSIFIER=

	[ALCHEMY]
	ALCHEMY_API_KEY=

	[WKS]
	WKS_MODEL_ID=    
	```

**Note:** You must perform the procedure in the `WKS` Jupyter notebook to generate the value for the `WKS_MODEL_ID` environment variable. Add the value to the `.env` file after you have created the WKS model as described in [Training an entity detection model](#training).

## <a name="running-notebooks"></a>Running the notebooks
The Jupyter notebooks show you step-by-step instructions, automatically executing specified sections of Python code. We used Jupyter notebooks because they encourage experimentation, which is an important part of developing any machine learning system.

To start the notebooks, make sure you are in the root directory of your git checkout of the SK repository, and run the command `jupyter notebook`. This  starts the Jupyter notebook server and opens a browser window. With the browser window open, click on notebooks, and then open the notebook labeled `Training`. Follow the instructions.

## <a name="training"></a>Training an entity detection model

The training phase is responsible for creating a customized model that detects entities related to the topic of the reviews. This model can be created by using Watson Knowledge Studio (WKS) for annotating the data (product reviews) to detect entities and their relationships.

The WKS tool exports a customized Alchemy model that is able to extract entities and relationships from unseen data. The steps to preprocess the data and create the models are detailed in the Jupyter notebooks under the `notebooks` folder of this repo.

To create your WKS model and export it to your Alchemy API key, follow the instructions in the `WKS` notebook.

After you have created your customized model, follow the instructions to train your classifier in the `Training` notebook.


## <a name="processing"></a>Processing the data

This step uses the models trained in the previous step by the `WKS` and `Training` notebooks and it can be achieved by following the `Processing` notebook. This is optional and you should only run it if you want to deploy the application locally using the UI provided in the repo using Cloudant in the persistence layer.

## Running the application locally

To deploy the application locally, run the command

    python server.py

The app will be listening on port 3000. Open a web browser and type

    localhost:3000

## <a name="adaptingextending-the-starter-kit"></a>Adapting/Extending the Starter Kit

<!--
<a>
# Architecture Diagram
</a>
-->

![](readme_images/VoC-ArchitectureFlow.jpg)

This Starter Kit works off of product reviews data gathered from Amazon product reviews (http://jmcauley.ucsd.edu/data/amazon/). However, the concepts used here are platform independent and can be applied to use cases other than electronic products reviews. Just define your use case and make sure you train your Natural Language Classifier accordingly by using the tool provided on the service page. Additionally, you can create your own customized models for entity extraction by using Watson Knowledge Studio and Alchemy.

## <a name="deploying"></a>Deploying the application to Bluemix

Push the updated application live by running the following command:

    cf push

or by pressing the "Deploy to Bluemix" button below.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/watson-developer-cloud/voice-of-the-customer.git)

## <a name="best-practices"></a>Best Practices

### Intents for the NLC service instance
  * When defining intents, follow naming conventions to create consistent intents.
  * Use "`-`" to separate multiple levels (Example: `location-weather-forecast`)
  * Use "`_`" to separate multiple word intents (Example: `business_center`)
  * Provide more variations of input via examples for each intent. The more variations the better.
  * Avoid overlapping intents across examples. (Example: `benefits_eligibility` and `benefits_eligibility_employee`). To avoid this, group examples into a single intent and use entities to deal with subtle variations.
  * Examples for intents should be representative of end user input.


## <a name="troubleshooting"></a>Troubleshooting

### Watson Knowledge Studio (WKS)
  * Entity and Relation Types can NOT have spaces. It is best to stick with alphanumeric characters and the underscore ("`_`") character.
  * At least 2 entity types and at least 2 relation types with 2 example mentions of each in the ground truth are required to perform a successful training run of machine learning annotator.
  * Rule of thumb: 50 mentions for a given type (entity type, relation type) in the training data. It is recommended to have training data distributed across all possible subtypes and roles for entities to help train system better.
  * When defining type system and document size, make sure that type system is not too complex and document size is not too large that human annotators won't be able to efficiently follow the guidelines. Keep the entity types to fewer than 50 and keep document size to no more than a few paragraphs.
  * Name entity and relation types in a way that is not ambiguous. If any names for entity or relation types are similar, it will make it more difficult to remember when to use which type.
  * For ground truth, it is recommended to use representative documents that include the entities and relations most relevant for your application. Representative really means that the mentions and relations appear in similar context (other words around them) as to what your application expects.

### Bluemix logs
To troubleshoot your Bluemix application, use the logs. To see the logs, run:

  ```bash
  cf logs <application-name> --recent
  ```

## <a name="ref"></a>Reference information

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
