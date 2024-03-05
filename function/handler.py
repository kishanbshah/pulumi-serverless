from datetime import datetime
import uuid
import json
import boto3

def handler(event, context):
    uuid_str = str(uuid.uuid4()) 
    file_content = datetime.now().isoformat()
    print("Invoking lambda for UUID: {}", uuid_str)
    try:
        # Get data to be written (replace with your actual data source)
        data = {
            "id": uuid_str,
            "data": file_content,
        }

        # S3 Interaction
        s3 = boto3.client('s3')
        bucket_name = "my-pulumi"  # Replace with your S3 bucket name
        file_name = f"data_{uuid_str}.json"  # Generate filename based on ID
        s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=file_name)

        # DynamoDB Interaction
        dynamodb = boto3.resource('dynamodb')
        table_name = "my-pulumi-table-794ebee"  # Replace with your DynamoDB table name
        table_content = {
            "id": uuid_str,
            "data": datetime.now().isoformat(),
            "fileName": file_name   
        }
        table = dynamodb.Table(table_name)
        table.put_item(Item=table_content)
        

        # Response
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    except Exception as e:
        print("Failed to upload to s3 for UUID {}, {}", uuid_str, e)

