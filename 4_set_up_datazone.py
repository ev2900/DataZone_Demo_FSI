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

datazone_domain_id = '<domain-id>'

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

# Define the secret detail
def create_redshift_secret(secret_name, project_name):
    try:
        response = smc.create_secret(
            Name = secret_name,
            SecretString = '{"username":"admin","password":"Pa$word1"}',
            Tags = [
                {
                    'Key': 'AmazonDataZoneDomain',
                    'Value': datazone_domain_id
                },
                {
                    'Key': 'AmazonDataZoneProject',
                    'Value': project_dict[project_name]
                }
            ]
        )
        
        redshift_login_secret_arn = response['ARN']
        print('Secret created: ' + redshift_login_secret_arn)
        
        return redshift_login_secret_arn
        
    except ClientError as e:
        print(e)
        
        response = smc.describe_secret(SecretId = secret_name)
        redshift_login_secret_arn = response['ARN']
        
        return redshift_login_secret_arn

investment_portfolio_redshift_secret_arn = create_redshift_secret('investment_portfolio_redshift_secret', 'Investment Portfolio')
loan_application_processing_redshift_secret_arn = create_redshift_secret('loan_application_processing_redshift_secret', 'Loan Application Processing')
market_data_and_insights_redshift_secret_arn = create_redshift_secret('market_data_and_insights_redshift_secret', 'Market Data and Insights')
regulatory_compliance_redshift_secret_arn = create_redshift_secret('regulatory_compliance_redshift_secret', 'Regulatory Compliance')
risk_management_redshift_secret_arn = create_redshift_secret('risk_management_redshift_secret', 'Risk Management')

def create_environment_redshift(env_name, project_name, workgroup_name, redshift_login_secret_arn):
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
create_environment_redshift('Investment Portfolio', 'Investment Portfolio', 'investment-portfolio', investment_portfolio_redshift_secret_arn)

# Loan Application Processing - Redshift
create_environment_redshift('Loan Application Processing', 'Loan Application Processing', 'loan-application-processing', loan_application_processing_redshift_secret_arn)

# Market Data and Insights - Redshift
create_environment_redshift('Market Data and Insights', 'Market Data and Insights', 'market-data-insights', market_data_and_insights_redshift_secret_arn)

# Regulatory Compliance - Redshift
create_environment_redshift('Regulatory Compliance', 'Regulatory Compliance', 'regulatory-compliance', regulatory_compliance_redshift_secret_arn)

# Risk Management - Redshift
create_environment_redshift('Risk Management', 'Risk Management', 'risk-management', risk_management_redshift_secret_arn)

#
# 5. Create a data source for each project
#

def get_enviorment_id(project_name):
    r = dzc.list_environments(domainIdentifier = datazone_domain_id, projectIdentifier = project_dict[project_name])

    return r['items'][0]['id']
    
#
# Data Lake Data Sources
#

def create_data_source_glue(data_source_name, project_name, glue_database_name):
    try:
        r = dzc.create_data_source(
            name = data_source_name,
            domainIdentifier = datazone_domain_id,
            environmentIdentifier = get_enviorment_id(project_name),
            projectIdentifier = project_dict[project_name],
            recommendation = {
                'enableBusinessNameGeneration': True
            },
            type = 'glue',
            configuration = {
                'glueRunConfiguration' : {
                'relationalFilterConfigurations': [
                    {
                        'databaseName': glue_database_name,
                        'filterExpressions': [
                        {
                            'expression': '*',
                            'type': 'INCLUDE'
                        }
                        ]
                    }
                ]
                }
            }
        )
        
        return r['id']
        
    except Exception as e:
        print(e)

data_source_ids = []

# Credit Scoring
data_source_ids.append(create_data_source_glue('Credit Scoring Glue Data Catalog', 'Credit Scoring', 'credit_scoring'))

# Customer Transaction
data_source_ids.append(create_data_source_glue('Customer Transaction Glue Data Catalog', 'Customer Transaction', 'customer_transaction'))

# Financial Reporting and Analytics
data_source_ids.append(create_data_source_glue('Financial Reporting and Analytics Glue Data Catalog', 'Financial Reporting and Analytics', 'financial_reporting_and_analytics'))

# Fraud Detection and Analysis
data_source_ids.append(create_data_source_glue('Fraud Detection and Analysis Glue Data Catalog', 'Fraud Detection and Analysis', 'fraud_detection_and_analysis'))

# Insurance Policy
data_source_ids.append(create_data_source_glue('Insurance Policy Glue Data Catalog', 'Insurance Policy', 'insurance_policy'))

#
# Redshift Data Sources
#

def create_data_source_redshift(data_source_name, project_name, redshift_serverless_workgroup_name, secret_arn):
    try:
        r = dzc.create_data_source(
            name = data_source_name,
            domainIdentifier = datazone_domain_id,
            environmentIdentifier = get_enviorment_id(project_name),
            projectIdentifier = project_dict[project_name],
            recommendation = {
                'enableBusinessNameGeneration': True
            },
            type = 'redshift',
            configuration = {
                'redshiftRunConfiguration': {
                    'redshiftCredentialConfiguration': {
                        'secretManagerArn': secret_arn
                    },
                    'redshiftStorage': {
                        'redshiftServerlessSource': {
                            'workgroupName': redshift_serverless_workgroup_name
                    }
                },
                
                'relationalFilterConfigurations': [
                    {
                        'databaseName': 'dev',
                        'filterExpressions': [
                            {
                                'expression': '*',
                                'type': 'INCLUDE'
                            },
                        ],
                        'schemaName': 'public'
                    },
                ]
            }
            }
        )
            
        return(r['id'])
            
    except Exception as e:
        print(e)

# Investment Portfolio
create_data_source_redshift('Investment Portfolio Redshift', 'Investment Portfolio', 'investment-portfolio', investment_portfolio_redshift_secret_arn)

# Loan Application Processing
create_data_source_redshift('Loan Application Processing Redshift', 'Loan Application Processing', 'loan-application-processing', loan_application_processing_redshift_secret_arn)

# Market Data and Insights
create_data_source_redshift('Market Data and Insights Redshift', 'Market Data and Insights', 'market-data-insights', market_data_and_insights_redshift_secret_arn)

# Regulatory Compliance
create_data_source_redshift('Regulatory Compliance Redshift', 'Regulatory Compliance', 'regulatory-compliance', regulatory_compliance_redshift_secret_arn)

# Risk Management
create_data_source_redshift('Risk Management Redshift', 'Risk Management', 'risk-management', risk_management_redshift_secret_arn)
