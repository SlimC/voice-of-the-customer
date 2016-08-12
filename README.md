# Product Intelligence Demo [![Build Status](https://travis.innovate.ibm.com/watson-developer-cloud/product-intelligence.svg?token=ouxuNEZVg24FqsCxcPYL)](https://travis.innovate.ibm.com/watson-developer-cloud/product-intelligence)

## Getting Started

1. Install the python dependencies with `pip`

    ```sh
    pip install -r requirements.txt
    ```

1. Install the node dependencies with `npm`

    ```sh
    npm install
    ```

1. Start the application

    ```sh
    npm start
    ```

### High Level Flow

Training 

1. Train WKS Model
2. Make training/testing sets
3. Do entity replacement on the training/testing sets
4. Design the NLC tree
5. Do the hand classification on the replaced training and testing set
6. Train the classifiers
7. Validate then troubleshoot if necessary

Processing (What the src/Processing/controller.py does)

1. Take review and run it through entity extraction
2. Run it through classifier
3. Cluster
4. make Final JSON actually turns this into something a front end can use


### Privacy Notice

This node sample web application includes code to track deployments to Bluemix and other Cloud Foundry platforms. The following information is sent to a [Deployment Tracker][deploy_track_url] service on each deployment:

* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris`)

This data is collected from the `VCAP_APPLICATION` environment variable in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

### Disabling Deployment Tracking

Deployment tracking can be disabled by removing `require('cf-deployment-tracker-client').track();` from the beginning of the `server.js` file at the root of this repo.