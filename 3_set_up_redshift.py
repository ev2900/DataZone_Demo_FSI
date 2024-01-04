import psycopg2 # pip install psycopg2-binary

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

# hosts
loan_application_processing_host = ''
regulator_compliance_host = ''
market_data_insights_host = ''
risk_management_host = ''
investment_portfolio_host = ''

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

    query = "COPY " + table_name + "FROM " + s3_bucket_path + "IAM_ROLE " + ____ + "CSV IGNOREHEADER 1 DELIMITER ','"

    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

# loan-application-processing
load_table(loan_application_processing_host, ,'loan_application_processing')
