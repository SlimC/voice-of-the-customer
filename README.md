# Product Intelligence Demo [![Build Status](https://travis.innovate.ibm.com/watson-developer-cloud/demo-boilerplate-nodejs.svg?token=ouxuNEZVg24FqsCxcPYL)](https://travis.innovate.ibm.com/watson-developer-cloud/demo-boilerplate-nodejs)

[TODO: ADD README TEXT]

### Privacy Notice

This node sample web application includes code to track deployments to Bluemix and other Cloud Foundry platforms. The following information is sent to a [Deployment Tracker][deploy_track_url] service on each deployment:

* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris`)

This data is collected from the `VCAP_APPLICATION` environment variable in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

### Disabling Deployment Tracking

Deployment tracking can be disabled by removing `require('cf-deployment-tracker-client').track();` from the beginning of the `server.js` file at the root of this repo.