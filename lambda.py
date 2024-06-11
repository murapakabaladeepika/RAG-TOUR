import json
import boto3
from datetime import datetime
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Read the content of the file
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read().decode('utf-8')

    # Append the current timestamp to the file content
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')
    new_file_content = f"{file_content}\nTimestamp: {timestamp}"

    # Define the new object key for the output folder
    output_key = f"output/{os.path.basename(object_key)}"

    # Save the new file content back to the S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=output_key, Body=new_file_content)

    return {
        'statusCode': 200,
        'body': json.dumps('File processed and saved successfully!')
    }
