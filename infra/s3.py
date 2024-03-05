import pulumi
from pulumi_aws import s3

class S3BucketComponent(pulumi.ComponentResource):
  def __init__(self, name, bucket_name, tags=None, opts=None):
    super().__init__('my-serverless-app:infra:S3Module',name, opts=opts)

    # Create the S3 bucket
    self.bucket = s3.Bucket(
        f"{name}-bucket",
        bucket=bucket_name,
        tags=tags,
        opts=pulumi.ResourceOptions(parent=self),
    )
