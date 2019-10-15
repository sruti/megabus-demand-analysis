import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('journeysTable')


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
