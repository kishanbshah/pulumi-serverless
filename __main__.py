import json
import pulumi
import pulumi_aws as aws
import pulumi_aws_apigateway as apigateway
from infra.s3 import S3BucketComponent
from infra.dynamodb import DynamoDBTableComponent

# Create an S3 bucket to receive file uploads
bucket_component = S3BucketComponent("s3-component", bucket_name="my-pulumi", tags={"Name": "My S3 Bucket"})

# Create a DynamoDB table with a simple primary key: filename
table_component = DynamoDBTableComponent(
    name="my-table-component",
    table_name="my-pulumi",
    attributes=[
        {"name": "id", "type": "S"}
    ],
    hash_key="id",
)

# An execution role to use for the Lambda function
role = aws.iam.Role("role", 
   assume_role_policy=json.dumps({
  'Version': '2012-10-17',
  'Statement': [
    {
      'Action': 'sts:AssumeRole',
      'Effect': 'Allow',
      'Principal': {
        'Service': 'lambda.amazonaws.com'
      }
    },
],
}),
managed_policy_arns=[aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE])

# creating an inline policy for lambda role
inline_policy = {
    "Version": "2012-10-17",
    "Statement": [    {
      'Effect': 'Allow',
      'Action': [
        's3:PutObject',
        's3:GetObject',
        's3:ListBucket'
      ],
      'Resource': [
        'arn:aws:s3:::my-pulumi',
        'arn:aws:s3:::my-pulumi/*'
      ]
    },
    {
      'Effect': 'Allow',
      'Action': [
        'dynamodb:PutItem',
        'dynamodb:GetItem',
        'dynamodb:UpdateItem',
        'dynamodb:BatchGetItem',
        'dynamodb:BatchWriteItem'
      ],
      'Resource': [
        'arn:aws:dynamodb:us-west-2:283328821634:table/my-pulumi-table-794ebee'
      ]
    }
]}


# Attach the inline policy to the IAM role
role_policy = aws.iam.RolePolicy('InlinePolicy',
                                 role=role.name,
                                 policy=inline_policy)


# A Lambda function to invoke
fn = aws.lambda_.Function('fn',
    runtime="python3.9",
    handler="handler.handler",
    role=role.arn,
    code=pulumi.FileArchive("./function"))

# A REST API to route requests to HTML content and the Lambda function
api = apigateway.RestAPI("api",
  routes=[
    apigateway.RouteArgs(path="/", local_path="www"),
    apigateway.RouteArgs(path="/pulumiTest", method=apigateway.Method.GET, event_handler=fn)
  ])

# The URL at which the REST API will be served.
pulumi.export("url", api.url)
