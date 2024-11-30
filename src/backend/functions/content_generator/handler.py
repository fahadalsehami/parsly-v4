import json
import boto3

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Content generation initiated',
                'input': body
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }