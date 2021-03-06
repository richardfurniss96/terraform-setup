import boto3
import random
import string


def dynamodb_create():
    dynamodb_client = boto3.client('dynamodb')

# Create the DynamoDB table.
    try:
        response = dynamodb_client.create_table(
            TableName='terraform_locks',
            KeySchema=[
                {
                    'AttributeName': 'LockID',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'LockID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    except dynamodb_client.exceptions.ResourceInUseException:
        print('A table called terraform_locks already exists')
        pass


def s3_backend_create(bucket_name=None, region_name='eu-west-2'):
    s3_client = boto3.client('s3', region_name='eu-west-2')

    # If the bucket_name isn't set it defaults to tfstates with a random 10 character ascii string.
    if bucket_name is None:
        letters = string.ascii_lowercase
        default_name = "tfstates-" + \
            ''.join(random.choice(letters) for i in range(10))
        s3_client.create_bucket(Bucket=default_name, CreateBucketConfiguration={
            'LocationConstraint': region_name})

        response_public = s3_client.put_public_access_block(
            Bucket=default_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
    # Otherwise it creates the bucket with the name defined
    else:
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': region_name})

        response_public = s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )


dynamodb_create()
# s3_backend_create()
