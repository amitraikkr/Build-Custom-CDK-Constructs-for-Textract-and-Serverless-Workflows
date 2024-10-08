import boto3
import os
import json
import time
from urllib.parse import unquote_plus
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define the region explicitly (or retrieve it from environment variables)
region = os.getenv('AWS_REGION', 'us-east-1')

# Create boto3 clients with the specific region
s3_client = boto3.client('s3', region_name=region)
textract_client = boto3.client('textract', region_name=region)
dynamodb_client = boto3.client('dynamodb', region_name=region)
sns_client = boto3.client('sns', region_name=region)

def handler(event, context):
    """
    Lambda function handler to process documents uploaded to S3.
    It uses Textract to extract text from the document, stores the result in DynamoDB,
    and optionally sends an SNS notification when processing is complete.
    """
    
    # Retrieve bucket name, DynamoDB table name, and SNS topic ARN from environment variables
    bucket_name = os.getenv('BUCKET_NAME')
    table_name = os.getenv('TABLE_NAME')
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
    
    logger.info("Received event: %s", json.dumps(event))
    
    try:
        # Parse S3 event to get object key
        s3_event = event['Records'][0]['s3']
        document_key = unquote_plus(s3_event['object']['key'])
        
        logger.info(f"Processing document from bucket: {bucket_name}, key: {document_key}")
        
        # Call Textract to extract text from the document
        response = textract_client.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }
            }
        )
        
        logger.info("Textract response received.")
        
        # Extract text from Textract response
        extracted_text = ''
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                extracted_text += item['Text'] + '\n'
        
        logger.info("Text extracted from document.")
        
        # Generate a timestamp and convert to string (seconds since epoch)
        timestamp = str(int(time.time()))
        
        # Store extracted text in DynamoDB
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'DocumentID': {'S': document_key},
                'ExtractedText': {'S': extracted_text},
                'Timestamp': {'S': timestamp}
            }
        )
        logger.info(f"Data successfully inserted into DynamoDB table: {table_name}")
    
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise  # Re-raise the exception after logging
    
    # Optional SNS notification
    if sns_topic_arn:
        try:
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=f"Document {document_key} processed and text extracted.",
                Subject="Textract Document Processing"
            )
            logger.info("SNS notification sent successfully.")
        except Exception as e:
            logger.error(f"Error sending SNS notification: {e}")
            raise  # Re-raise the exception after logging
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Document {document_key} processed successfully.")
    }