import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('WebsiteUptimeLogs')

    start_key = json.loads(event['queryStringParameters'].get('start_key', 'null'))

    netflix_response = table.query(
        KeyConditionExpression='URL = :url',
        ExpressionAttributeValues={':url': 'https://www.netflix.com/'},
        ScanIndexForward=False,
        Limit=5,
        ExclusiveStartKey=start_key if start_key else None
    )

    netflix_items = netflix_response['Items']
    netflix_last_evaluated_key = netflix_response.get('LastEvaluatedKey')

    netflix_response = table.query(
        KeyConditionExpression='URL = :url',
        ExpressionAttributeValues={':url': 'https://www.netflix.com/'},
        ScanIndexForward=False,
        Limit=5,
        ExclusiveStartKey=start_key if start_key else None
    )

    netflix_items = netflix_response['Items']
    netflix_last_evaluated_key = netflix_response.get('LastEvaluatedKey')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'netflix_items': netflix_items,
            'netflix_lastEvaluatedKey': netflix_last_evaluated_key
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
