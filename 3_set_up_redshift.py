import psycopg2 # pip install psycopg2-binary

# Connect to Redshift
conn = psycopg2.connect(
    dbname = 'dev',
    user = 'admin',
    password = 'Pa$word1',
    host = 'risk-management.001507382070.us-east-1.redshift-serverless.amazonaws.com',
    port='5439'  # Default Redshift port
)

# Execute query
cur = conn.cursor()

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

cur.execute(query)

# For a SELECT query, you might want to fetch results
results = cur.fetchall()
print(results)

conn.commit()
cur.close()
conn.close()
