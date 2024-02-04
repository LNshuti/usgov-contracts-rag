from snowflake.connector import connect
import csv
import os 

# Define the Snowflake account, user, password, warehouse, and database
account = os.environ['SNOWFLAKE_ACCOUNT']
user = os.environ['SNOWFLAKE_USER']
password = os.environ['SNOWFLAKE_PASSWORD']
warehouse = os.environ['SNOWFLAKE_WAREHOUSE']
database = os.environ['SNOWFLAKE_DATABASE']
schema = os.environ['SNOWFLAKE_SCHEMA']

#sf = Snowflake(account, user, password, warehouse, database)

# Establish a connection to the Snowflake database
conn = connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema='DEMO_SCHEMA'
)

# Load the CSV file from S3
bucket = 'govgptco'
file_path = 'FY2023_archived_opportunities.csv'
conn.load_file(bucket, file_path, format='CSV')

# Create a table in Snowflake to store the loaded data
table_name = 'FY2023_archived_opportunities'
conn.create_table(table_name, column_definitions=None)

# Load the data into the table
conn.load_data(table_name, overwrite=True)

# Close the Snowflake connection
conn.close()