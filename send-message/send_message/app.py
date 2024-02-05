import json
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    try:
        message = json.loads(event['body'])

        # Validate metadata fields
        required_metadata_fields = ['message_time', 'company_id', 'message_id']
        if not all(field in message['metadata'] for field in required_metadata_fields):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid message. Missing required metadata fields.'})
            }

        # Save message to S3
        bucket_name = 'myawsmessage'
        s3_key = f"{message['metadata']['company_id']}/{message['metadata']['message_id']}.json"
        s3_client.put_object(Body=json.dumps(message), Bucket=bucket_name, Key=s3_key)

        # Save message to DynamoDB
        dynamodb_table = 'message_test_table'
        dynamodb_client.put_item(TableName=dynamodb_table, Item={'message_id': {'S': message['metadata']['message_id']}, 'data': {'S': json.dumps(message)}})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message processed successfully.'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }