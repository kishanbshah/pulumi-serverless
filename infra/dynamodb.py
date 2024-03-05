import pulumi
import pulumi_aws as aws

class DynamoDBTableComponent(pulumi.ComponentResource):
  def __init__(self, name, table_name, attributes, hash_key, opts=None):
    super().__init__('my-serverless-app:infra:DynamoDBTableComponent',name, opts=opts)

    # Define the table schema
    table_schema = []
    for attr in attributes:
      table_schema.append(aws.dynamodb.TableAttributeArgs(name=attr["name"], type=attr["type"]))

    # Create the DynamoDB table
    self.table = aws.dynamodb.Table(
        f"{table_name}-table",
        attributes=table_schema,
        hash_key=hash_key,
        billing_mode="PAY_PER_REQUEST",
        opts=pulumi.ResourceOptions(parent=self),
    )