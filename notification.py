import boto3
import os

aws_account = os.environ.get("AWS_ACCOUNT_ID")
region = os.environ.get("REGION")

sns = boto3.resource('sns')
topic = sns.Topic(
    'arn:aws:sns:{}:{}:scrape-parameters'.format(region, aws_account))


def send_scrape_params(message):
    response = topic.publish(Message=message)
    return response
