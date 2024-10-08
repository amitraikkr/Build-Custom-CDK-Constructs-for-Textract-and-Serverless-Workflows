import aws_cdk as cdk
from aws_cdk import assertions
from cdk_construct_custom.textract_construct import DocumentExtractConstructProps, DocumentExtractConstruct
from cdk_construct_custom.cdk_construct_custom_stack import CdkConstructCustomStack

def test_textract_construct():
    # Create the app and stack
    app = cdk.App()
    stack = cdk.Stack(app, "TestStack")
    
    # Create the custom construct with minimal props
    DocumentExtractConstruct(
        stack, 
        "TestConstruct",
        props=DocumentExtractConstructProps(
            lambda_props={"runtime": cdk.aws_lambda.Runtime.PYTHON_3_8},
            s3_props={},
            dynamodb_props={}
        )
    )

    # Prepare the stack for assertions
    template = assertions.Template.from_stack(stack)

    # Assert that the S3 bucket is created with versioning enabled
    template.has_resource_properties("AWS::S3::Bucket", {
        "VersioningConfiguration": {
            "Status": "Enabled"
        }
    })

    # Assert that the Lambda function has the correct properties
    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.8",
        "MemorySize": 1024
    })

    # Assert that the DynamoDB table is created
    template.resource_count_is("AWS::DynamoDB::Table", 1)