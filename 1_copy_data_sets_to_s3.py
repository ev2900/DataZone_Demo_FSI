
#
# 0. Install / import boto3 and os libraries
#

import os
import boto3 # pip install boto3

#
# 1. Get CloudFormation output
#

cfn = boto3.client('cloudformation')

# Set the name of the CloudFormation stack
stack_name = 'c-0-loudformation'

response = cfn.describe_stacks(StackName=stack_name)

for stack in response['Stacks']:
    if stack["StackName"] == stack_name:
        for output in stack["Outputs"]:
            if output["OutputKey"] == "IAMRoleARN":
                IAMRoleARN = output["OutputValue"]
                
            elif output["OutputKey"] == "S3BucketARN":
                s3_bucket_arn = output["OutputValue"]
                s3_bucket_name = s3_bucket_arn.split(':')[-1]

#
# 2. Get the account id
#

stsc = boto3.client('sts')

caller_identity = stsc.get_caller_identity()
account_id = caller_identity.get('Account')

#
# 3. Set DataLake Admin, Change defaulr IAM access control for new databases and tables
# 

lfc = boto3.client('lakeformation')

data_lake_settings = {'DataLakeAdmins': [{'DataLakePrincipalIdentifier': 'arn:aws:iam::' + account_id + ':role/Admin'}], 'CreateDatabaseDefaultPermissions': [], 'CreateTableDefaultPermissions': []}

lfc.put_data_lake_settings(DataLakeSettings = data_lake_settings)

# 
# 4. Register DataLake Location - Administration
# 

lfc = boto3.client('lakeformation')

try:
    lfc.register_resource(ResourceArn = s3_bucket_arn, UseServiceLinkedRole = True) # --no-hybrid-access-enabled ?
except lfc.exceptions.AlreadyExistsException:
    print('The s3 bucket ' + s3_bucket_arn + ' is already registered with LakeFormation')
