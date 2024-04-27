import requests
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebsiteUptimeLogs')

def lambda_handler(event, context):
    websites = ['https://www.netflix.com/', 'http://example.org']
    results = []

    for url in websites:
        try:
            response = requests.get(url)
            result = {'url': url, 'status': response.status_code, 'timestamp': datetime.now().isoformat()}
            results.append(result)
            table.put_item(Item=result)
        except Exception as e:
            results.append({'url': url, 'error': str(e), 'timestamp': datetime.now().isoformat()})

    return results