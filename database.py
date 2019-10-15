import boto3
import os

aws_account = os.environ.get("AWS_ACCOUNT_ID")
region = os.environ.get("REGION")
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('journeysTable')

sns = boto3.resource('sns')
topic = sns.Topic(
    'arn:aws:sns:{}:{}:scrape-parameters'.format(region, aws_account))


def get_journey(journey_id):
    response = table.get_item(Key={'journey_id': journey_id})
    journey = response.get("Item")
    return journey


def put_journey(journey):
    response = table.put_item(Item=journey)
    return response


def update_journey(journey_id, price_by_numtix):
    response = table.update_item(Key={'journey_id': journey_id},
                                 UpdateExpression='SET price_by_numtix = :pbc',
                                 ExpressionAttributeValues={
        ':pbc': price_by_numtix
    })
    return response


def publish_sns(message):
    response = topic.publish(Message=message)
    return response
