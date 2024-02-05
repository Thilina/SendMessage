import json
import boto3
from botocore.exceptions import ClientError

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        message_id = data['message_id']

        # Retrieve message from DynamoDB
        dynamodb_table = 'your-dynamodb-table'
        response = dynamodb_client.get_item(TableName=dynamodb_table, Key={'message_id': {'S': message_id}})

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Message not found.'})
            }

        return {
            'statusCode': 200,
            'body': response['Item']['data']['S']
        }

    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing message_id parameter.'})
        }

    except ClientError as e:
        return {
            'statusCode': e.response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps({'error': e.response['Error']['Message']})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }