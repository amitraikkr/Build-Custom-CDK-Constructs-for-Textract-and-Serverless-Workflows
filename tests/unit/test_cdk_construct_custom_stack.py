import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_construct_custom.cdk_construct_custom_stack import CdkConstructCustomStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_construct_custom/cdk_construct_custom_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkConstructCustomStack(app, "cdk-construct-custom")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
