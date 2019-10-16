# Megabus Demand Analysis
A simple program to regularly get data from Megabus to understand demand (currently only for Edinburgh to London route).
Deployed in AWS using the Serverless framework. 
Uses Sentry for error handling.

![Architecture Diagram](https://github.com/sruti/megabus-demand-analysis/architecture.jpg)

## Setup
Install [Serverless](https://serverless.com/framework/docs/getting-started/)
```
npm install serverless
```
Deploy the service
```
sls deploy
```

## To Run
Scrape for a specific date (modify the date in sample_sns_message.txt)
```
sls invoke -f scrape_megabus -p sample_sns_message.txt
```
Trigger scrape for all dates for Edinburgh to London route
```
sls invoke -f trigger_scrape_megabus
```
Go to journeysTable DynamoDB table in the AWS console and click on an item to see the new data