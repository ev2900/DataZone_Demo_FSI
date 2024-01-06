import psycopg2 # pip install psycopg2-binary
import boto3

# Define function to run a SQL query on Redshift
def run_sql(host, query):
    
    # Connect to Redshift
    conn = psycopg2.connect(
        dbname = 'dev',
        user = 'admin',
        password = 'Pa$word1',
        host = host,
        port='5439'  # Default Redshift port
    )

    # Execute query
    cur = conn.cursor()

    cur.execute(query)

    # For a SELECT query, you might want to fetch results
    #results = cur.fetchall()
    #print(results)

    conn.commit()
    cur.close()
    conn.close()

# Define a function to get the endpoint of a Redshift serverless instance
rssc = boto3.client('redshift-serverless')

def get_redshift_serverless_endpoint(workgroup_name):
    r = rssc.get_workgroup(workgroupName = workgroup_name)
    return r['workgroup']['endpoint']['address']

# hosts
loan_application_processing_host = get_redshift_serverless_endpoint('loan-application-processing')
regulator_compliance_host = get_redshift_serverless_endpoint('regulatory-compliance')
market_data_insights_host = get_redshift_serverless_endpoint('market-data-insights')
risk_management_host = get_redshift_serverless_endpoint('risk-management')
investment_portfolio_host = get_redshift_serverless_endpoint('investment-portfolio')

## Create Tables

# loan-application-processing
query = '''CREATE TABLE loan_application_processing (
    ApplicationID VARCHAR(20),
    CustomerID VARCHAR(15),
    ApplicationDate DATE,
    LoanType VARCHAR(20),
    LoanAmount DECIMAL(12, 2),
    LoanTerm INT,
    InterestRate DECIMAL(5, 2),
    CreditScore INT,
    ApprovalStatus VARCHAR(15),
    ProcessingTime INT
);'''

run_sql(loan_application_processing_host, query)

# regulatory-compliance
query = '''CREATE TABLE regulatory_compliance (
    ComplianceID VARCHAR(15),
    CustomerID VARCHAR(10),
    RegulationType VARCHAR(20),
    ComplianceStatus VARCHAR(15),
    ReviewDate DATE,
    Country VARCHAR(20),
    PenaltyAmount DECIMAL(12, 2),
    NextReviewDate DATE
);'''

run_sql(regulator_compliance_host, query)

# market-data-insights
query = '''CREATE TABLE market_data_insights (
    DataID VARCHAR(20),
    MarketType VARCHAR(20),
    Symbol VARCHAR(10),
    OpenPrice DECIMAL(14, 2),
    ClosePrice DECIMAL(14, 2),
    HighPrice DECIMAL(14, 2),
    LowPrice DECIMAL(14, 2),
    Volume BIGINT,
    Date DATE,
    Country VARCHAR(20)
);'''

run_sql(market_data_insights_host, query)

# risk-management
query = '''CREATE TABLE risk_management (
    RiskID VARCHAR(10),
    CustomerID VARCHAR(10),
    RiskType VARCHAR(20),
    RiskScore INT,
    ExposureAmount DECIMAL(12, 2),
    MitigationActions VARCHAR(30),
    ReviewDate DATE,
    RiskStatus VARCHAR(15)
);'''

run_sql(risk_management_host, query)

# investment-portfolio
query = '''CREATE TABLE investment_portfolio (
    CustomerID VARCHAR(15),
    PortfolioID VARCHAR(20),
    AssetType VARCHAR(20),
    AssetName VARCHAR(30),
    Quantity BIGINT,
    PurchasePrice DECIMAL(14, 2),
    CurrentPrice DECIMAL(14, 2),
    PurchaseDate DATE,
    Country VARCHAR(20)
);'''

run_sql(investment_portfolio_host, query)

## Load Tables

# Get IAM role from CloudFormation outputs
import boto3

cfn = boto3.client('cloudformation')

# Set the name of the CloudFormation stack
stack_name = 'data-zone-fsi'
response = cfn.describe_stacks(StackName=stack_name)

for stack in response['Stacks']:
    if stack["StackName"] == stack_name:
        for output in stack["Outputs"]:
            if output["OutputKey"] == "IAMRoleARNRedshift":
                IAMRoleARN = output["OutputValue"]
            elif output["OutputKey"] == "S3BucketARN":
                s3_bucket_arn = output["OutputValue"]
                s3_bucket_name = s3_bucket_arn.split(':')[-1]

# Define function to load Redshift tables
def load_table(host, s3_bucket_path, table_name):
    
    # Connect to Redshift
    conn = psycopg2.connect(
        dbname = 'dev',
        user = 'admin',
        password = 'Pa$word1',
        host = host,
        port='5439'  # Default Redshift port
    )

    # Execute query
    cur = conn.cursor()

    query = "COPY " + table_name + " FROM " + "'s3://" + s3_bucket_name + s3_bucket_path + "' IAM_ROLE '" + IAMRoleARN + "' CSV IGNOREHEADER 1 DELIMITER ','"

    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

# loan-application-processing
load_table(loan_application_processing_host, '/Loan_Application_Processing/Loan_Application_Processing_Data_Sample.csv', 'loan_application_processing')

# regulatory-compliance
load_table(regulator_compliance_host, '/Regulatory_Compliance/Regulatory_Compliance_Data_Sample.csv', 'regulatory_compliance')

# market-data-insights
load_table(market_data_insights_host, '/Market_Data_and_Insights/Market_Data_and_Insights_Sample.csv', 'market_data_insights')

# risk-management
load_table(risk_management_host, '/Risk_Management/Risk_Management_Data_Sample.csv', 'risk_management')

# investment-portfolio
load_table(investment_portfolio_host, '/Investment_Portfolio/Investment_Portfolio_Data_Sample.csv', 'investment_portfolio')
