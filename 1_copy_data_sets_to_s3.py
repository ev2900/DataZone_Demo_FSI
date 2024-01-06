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
stack_name = 'data-zone-fsi'

response = cfn.describe_stacks(StackName=stack_name)

for stack in response['Stacks']:
    if stack["StackName"] == stack_name:
        for output in stack["Outputs"]:               
            if output["OutputKey"] == "S3BucketARN":
                s3_bucket_arn = output["OutputValue"]
                s3_bucket_name = s3_bucket_arn.split(':')[-1]

#
# 2. Upload the Sample Data to S3
#

s3c = boto3.client('s3')

s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Credit_Scoring/Credit_Scoring_Data_Sample.csv', s3_bucket_name, 'Credit_Scoring/Credit_Scoring_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Customer_Transaction/Customer_Transaction_Data_Sample.csv', s3_bucket_name, 'Customer_Transaction/Customer_Transaction_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Financial_Reporting_and_Analytics/Financial_Reporting_and_Analytics_Data_Sample.csv', s3_bucket_name, 'Financial_Reporting_and_Analytics/Financial_Reporting_and_Analytics_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Fraud_Detection_and_Analysis/Fraud_Detection_and_Analysis_Data_Sample.csv', s3_bucket_name, 'Fraud_Detection_and_Analysis/Fraud_Detection_and_Analysis_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Insurance_Policy/Insurance_Policy_Data_Sample.csv', s3_bucket_name, 'Insurance_Policy/Insurance_Policy_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Investment_Portfolio/Investment_Portfolio_Data_Sample.csv', s3_bucket_name, 'Investment_Portfolio/Investment_Portfolio_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Loan_Application_Processing/Loan_Application_Processing_Data_Sample.csv', s3_bucket_name, 'Loan_Application_Processing/Loan_Application_Processing_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Market_Data_and_Insights/Market_Data_and_Insights_Sample.csv', s3_bucket_name, 'Market_Data_and_Insights/Market_Data_and_Insights_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Regulatory_Compliance/Regulatory_Compliance_Data_Sample.csv', s3_bucket_name, 'Regulatory_Compliance/Regulatory_Compliance_Data_Sample.csv')
s3c.upload_file('./DataZone_Demo_FSI/Data_Sets/Risk_Management/Risk_Management_Data_Sample.csv', s3_bucket_name, 'Risk_Management/Risk_Management_Data_Sample.csv')
