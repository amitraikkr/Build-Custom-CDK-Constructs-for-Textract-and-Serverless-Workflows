from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_iam as iam,
    aws_s3_notifications as s3n,

    Duration,
    RemovalPolicy
)
from constructs import Construct

class DocumentExtractConstructProps:
    def __init__(self, 
                email_id: str = None,
                lambda_props: dict = None,
                s3_props: dict = None,
                dynamodb_props: dict = None,
                sns_props: dict = None,
                iam_principal: iam.IPrincipal = None):
        self.email_id = email_id
        self.lambda_props = lambda_props
        self.s3_props = s3_props
        self.dynamodb_props = dynamodb_props
        self.sns_props = sns_props
        self.iam_principal = iam_principal

class DocumentExtractConstruct(Construct):
    def __init__(self, scope: Construct, id: str, props: DocumentExtractConstructProps, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Validation: Ensure required properties are provided
        if not props.lambda_props or not props.s3_props or not props.dynamodb_props:
            raise ValueError("lambda_props, s3_props, and dynamodb_props must be provided")

        # S3 Bucket
        bucket = s3.Bucket(self, "DocExtractBucket",
            **(props.s3_props or {
                "versioned": True,
                "removal_policy": RemovalPolicy.DESTROY,
                "auto_delete_objects": True
            })
        )

        # Bucket Policy
        if props.iam_principal:
            bucket.add_to_resource_policy(
                iam.PolicyStatement(
                    actions=["s3:PutObject", "s3:GetObject"],
                    resources=[f"{bucket.bucket_arn}/*"],
                    principals=[props.iam_principal]
                )
            )

        # SNS Topic
        sns_topic_arn = None
        if props.email_id:
            sns_topic = sns.Topic(self, "DocExtractSNS", **(props.sns_props or {}))
            sns_topic.add_subscription(subs.EmailSubscription(props.email_id))
            sns_topic_arn = sns_topic.topic_arn

        # DynamoDB Table
        dynamo_table = dynamodb.Table(self, "DocExtractDynamodbTable",
            partition_key=dynamodb.Attribute(
                name=props.dynamodb_props.get('partitionKey', 'DocumentID'),
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=(dynamodb.Attribute(name=props.dynamodb_props['sortKey'],
                type=dynamodb.AttributeType.STRING) if 'sortKey' in props.dynamodb_props else None),
            table_name=props.dynamodb_props.get('tableName', 'MyTable'),
            removal_policy=(RemovalPolicy.RETAIN if props.dynamodb_props.get('retainTable', False) else RemovalPolicy.DESTROY),
            billing_mode=props.dynamodb_props.get('billing_mode', dynamodb.BillingMode.PAY_PER_REQUEST),
            time_to_live_attribute=props.dynamodb_props.get('ttlAttribute', None) if props.dynamodb_props.get('enableTtl', False) else None   
        )

        # Lambda Function
        lambda_fn = _lambda.Function(self, "DocExtractLambdaFunction", 
            runtime=props.lambda_props.get('runtime', _lambda.Runtime.PYTHON_3_11),
            handler=props.lambda_props.get('handler', 'index.handler'),
            code=_lambda.Code.from_asset(props.lambda_props.get('code_asset', 'lambda')),
            memory_size=props.lambda_props.get('memory_size', 1024),
            timeout=Duration.seconds(props.lambda_props.get('timeout', 300)),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TABLE_NAME": dynamo_table.table_name,
                "SNS_TOPIC_ARN": sns_topic_arn or "",
                **props.lambda_props.get('environment', {})    
            }
        )

        # Grant necessary permissions for Textract
        lambda_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["textract:DetectDocumentText"],
                resources=[bucket.bucket_arn]  # Restrict to bucket ARN
            )
        )

        # S3 event notification to trigger Lambda
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda_fn)
        )

        # Grant permissions
        bucket.grant_read_write(lambda_fn)
        dynamo_table.grant_full_access(lambda_fn)
        if props.email_id:
            sns_topic.grant_publish(lambda_fn)