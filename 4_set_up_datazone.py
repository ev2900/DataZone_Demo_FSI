#
# 0. Install / import boto3 and os libraries
#

import os
import boto3 # pip install boto3
import time
from botocore.exceptions import ClientError

#
# 1. Get the account id
#

stsc = boto3.client('sts')

caller_identity = stsc.get_caller_identity()
account_id = caller_identity.get('Account')

#
# 2. via. the AWS protal create a DataZone domain. Click the quick set up box
#

datazone_domain_id = 'dzd_44l3dtago8pxuv'

#
# 3. Create DataZone projects
#

dzc = boto3.client('datazone')

def create_project(project_name):
    try:
        r = dzc.create_project(
            domainIdentifier = datazone_domain_id,
            name = project_name
        )
    except Exception as e:
        print(e)

create_project('Credit Scoring')
create_project('Customer Transaction')
create_project('Financial Reporting and Analytics')
create_project('Fraud Detection and Analysis')
create_project('Insurance Policy')
create_project('Investment Portfolio')
create_project('Loan Application Processing')
create_project('Market Data and Insights')
create_project('Regulatory Compliance')
create_project('Risk Management')

##time.sleep(120)

#
# 3. Get the id of the projects in DataZone
#

dzc = boto3.client('datazone')

project_dict = {}

r = dzc.list_projects(domainIdentifier = datazone_domain_id)

for project in r['items']:
    project_dict[project['name']] = project['id']

#
# 4. Create an enviorment for each project
#

# Get the ID of each enviorment profile
enviorment_profile_dict = {}

r = dzc.list_environment_profiles(domainIdentifier = datazone_domain_id)

for envioronment_profile in r['items']:
    enviorment_profile_dict[envioronment_profile['name']] = envioronment_profile['id']

# Create the enviorments
def create_environment_data_lake(env_name, project_name):
    try:
        r = dzc.create_environment(
            domainIdentifier = datazone_domain_id,
            environmentProfileIdentifier = enviorment_profile_dict['DataLakeProfile'],
            name = env_name,
            projectIdentifier = project_dict[project_name]
        )
    except Exception as e:
        print(e)

#
# Data Lake Enviorments
#
    
# Credit Scoring - Glue
create_environment_data_lake('Credit Scoring', 'Credit Scoring')

# Customer Transaction - Glue
create_environment_data_lake('Customer Transaction', 'Customer Transaction')

# Financial Reporting and Analytics - Glue
create_environment_data_lake('Financial Reporting and Analytics', 'Financial Reporting and Analytics')

# Fraud Detection and Analysis - Glue
create_environment_data_lake('Fraud Detection and Analysis', 'Fraud Detection and Analysis')

# Insurance Policy - Glue
create_environment_data_lake('Insurance Policy', 'Insurance Policy')

#
# Redshift Enviorments
#

# Create a secret manager secret with the Redshift login(s)
smc = boto3.client('secretsmanager')

# Define the secret details
try:
    response = smc.create_secret(
        Name = 'redshift-login',
        SecretString = '{"username":"admin","password":"Pa$word1"}'
    )
    
    redshift_login_secret_arn = response['ARN']
    print('Secret created: ' + redshift_login_secret_arn)
    
except ClientError as e:
    print(e)
    
    response = smc.describe_secret(SecretId = 'redshift-login')
    redshift_login_secret_arn = response['ARN']

def create_environment_redshift(env_name, project_name, workgroup_name):
    try:
        r = dzc.create_environment(
            domainIdentifier = datazone_domain_id,
            environmentProfileIdentifier = enviorment_profile_dict['DataWarehouseProfile'],
            name = env_name,
            projectIdentifier = project_dict[project_name],
            userParameters = [{'name': 'dataAccessSecretsArn', 'value': redshift_login_secret_arn}, {'name': 'dbName', 'value': 'dev'}, {'name': 'workgroupName', 'value': workgroup_name}]
        )
    except Exception as e:
        print(e)

# Investment Portfolio - Redshift
create_environment_redshift('Investment Portfolio', 'Investment Portfolio', 'investment-portfolio')

# Loan Application Processing - Redshift
create_environment_redshift('Loan Application Processing', 'Loan Application Processing', 'loan-application-processing')

# Market Data and Insights - Redshift
create_environment_redshift('Market Data and Insights', 'Market Data and Insights', 'market-data-insights')

# Regulatory Compliance - Redshift
create_environment_redshift('Regulatory Compliance', 'Regulatory Compliance', 'regulatory-compliance')

# Risk Management - Redshift
create_environment_redshift('Risk Management', 'Risk Management', 'risk-management')
