import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('servicesTable')


def get_data(service_id):
    response = table.get_item(Key={'service_id': service_id})
    data = response.get("Item")
    return data


def put_data(data):
    response = table.put_item(Item=data)
    return response


def update_data(service_id, price_by_capacity):
    response = table.put_item(Key={'service_id': service_id},
                              UpdateExpression='SET price_by_capacity = :pbc',
                              ExpressionAttributeValues={
        ':pbc': price_by_capacity
    })
    return response


def set_service_id(origin, destination, start_time, end_time):
    return origin + destination + start_time[0:2] + start_time[3:5] + end_time[0:2] + end_time[3:5]


def extract_service_id(service_id):
    return {
        "origin": service_id[0:2],
        "destination": service_id[2:4],
        "start_time": service_id[4:6] + ':' + service_id[6:8],
        "end_time": service_id[8:10] + ':' + service_id[10:12],
    }
