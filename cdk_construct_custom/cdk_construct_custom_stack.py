from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_sns as sns,
    RemovalPolicy
)
from constructs import Construct
from lib.textract_construct import DocumentExtractConstructProps, DocumentExtractConstruct

class CdkConstructCustomStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app_construct_props = DocumentExtractConstructProps(
            email_id ="amitraikkr760@gmail.com",

            lambda_props={
                "runtime":_lambda.Runtime.PYTHON_3_11,
                "memory_size": 1024,
                "timeout": 300,
                "code_asset":"lambda",
                "handler":"process_document.handler",
                "environment":{
                    "CUSTOM_ENV_VAR":"example_value"
                }
            },

            s3_props={
                "versioned":True,
                "encryption":s3.BucketEncryption.S3_MANAGED,
                "removal_policy": RemovalPolicy.DESTROY
            },

            dynamodb_props={
                "partitionKey":"DocumentID",
                "sortKey":"Timestamp",
                "tableName":"DocumentProcessingTable",
                "retainTable":False,
                "billing_mode": dynamodb.BillingMode.PAY_PER_REQUEST,
                "enableTtl":True,
                "ttlAttribute":"ExpirationTime"
            }
        )

        generic_app_construct=DocumentExtractConstruct(
            self,
            "DocumentProcessingApp",
            props=app_construct_props
        )

