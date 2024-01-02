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

data_lake_settings = {'DataLakeAdmins': [{'DataLakePrincipalIdentifier': 'arn:aws:iam::' + account_id + ':role/WSOpsRole'}], 'CreateDatabaseDefaultPermissions': [], 'CreateTableDefaultPermissions': []}

lfc.put_data_lake_settings(DataLakeSettings = data_lake_settings)

# 
# 4. Register DataLake Location - Administration
# 

lfc = boto3.client('lakeformation')

try:
    lfc.register_resource(ResourceArn = s3_bucket_arn, UseServiceLinkedRole = True) # --no-hybrid-access-enabled ?
except lfc.exceptions.AlreadyExistsException:
    print('The s3 bucket ' + s3_bucket_arn + ' is already registered with LakeFormation')

#
# 5. Create Glue Data Catalog Databases
#

gluec = boto3.client('glue')

def create_glue_database(database_name):
    try:
        gluec.create_database(DatabaseInput = {'Name': database_name})
    except gluec.exceptions.AlreadyExistsException:
        print('The ' + database_name + ' database already exists in the Glue data catalog')
    
create_glue_database('Credit_Scoring')
create_glue_database('Customer_Transaction')
create_glue_database('Financial_Reporting_and_Analytics')
create_glue_database('Fraud_Detection_and_Analysis')
create_glue_database('Insurance_Policy')
#create_glue_database('Investment_Portfolio')
#create_glue_database('Loan_Application_Processing')
#create_glue_database('Market_Data_and_Insights')
#create_glue_database('Regulatory_Compliance')
#create_glue_database('Risk_Management')

#
# 6. Data LakeFormation premissions to crawler IAM role
#

lfc = boto3.client('lakeformation')

# Premissions on S3 bucket
data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
resource = {'DataLocation': {'ResourceArn': s3_bucket_arn}}
permissions = ['DATA_LOCATION_ACCESS']

lfc.grant_permissions(
    Principal = data_lake_principal,
    Resource = resource,
    Permissions = permissions
)

# CREATE_TABLE on databases
def update_lakeformation_premissions_w_CREATE_TABLE(database_name):
    data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
    resource = {'Database': {'Name': database_name}}
    permissions = ['CREATE_TABLE']

    lfc.grant_permissions(
        Principal = data_lake_principal,
        Resource = resource,
        Permissions = permissions
    )

update_lakeformation_premissions_w_CREATE_TABLE('Credit_Scoring')
update_lakeformation_premissions_w_CREATE_TABLE('Customer_Transaction')
update_lakeformation_premissions_w_CREATE_TABLE('Financial_Reporting_and_Analytics')
update_lakeformation_premissions_w_CREATE_TABLE('Fraud_Detection_and_Analysis')
update_lakeformation_premissions_w_CREATE_TABLE('Insurance_Policy')

#
# 7. Create Glue crawlers
#

gluec = boto3.client('glue')

def create_glue_crawler(crawler_name, output_database_name, s3_path_to_crawl):
    try:
        gluec.create_crawler(
            Name = crawler_name,
            Role = IAMRoleARN,
            DatabaseName = output_database_name,
            Targets = {'S3Targets': [{'Path': s3_path_to_crawl}]}
        )
    except gluec.exceptions.AlreadyExistsException:
        print('Crawler ' + crawler_name + ' already exists')
        

create_glue_crawler('Credit_Scoring_Crawler', 'Credit_Scoring', 's3://' + s3_bucket_name + '/Credit_Scoring/')
create_glue_crawler('Customer_Transaction_Crawler', 'Customer_Transaction', 's3://' + s3_bucket_name + '/Customer_Transaction/')
create_glue_crawler('Financial_Reporting_and_Analytics_Crawler', 'Financial_Reporting_and_Analytics', 's3://' + s3_bucket_name + '/Financial_Reporting_and_Analytics/')
create_glue_crawler('Fraud_Detection_and_Analysis_Crawler', 'Fraud_Detection_and_Analysis', 's3://' + s3_bucket_name + '/Fraud_Detection_and_Analysis/')
create_glue_crawler('Insurance_Policy_Crawler', 'Insurance_Policy', 's3://' + s3_bucket_name + '/Insurance_Policy/')

#
# 8. Run Glue Crawlers
#

gluec = boto3.client('glue')

def run_glue_crawler(crawler_name):
    try:
        gluec.start_crawler(Name = crawler_name)
    except Exception as e:
        print(e)

run_glue_crawler('Credit_Scoring_Crawler')
run_glue_crawler('Customer_Transaction_Crawler')
run_glue_crawler('Financial_Reporting_and_Analytics_Crawler')
run_glue_crawler('Fraud_Detection_and_Analysis_Crawler')
run_glue_crawler('Insurance_Policy_Crawler')
