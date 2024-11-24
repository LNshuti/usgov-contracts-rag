import sqlite3
import pandas as pd
import openpyxl 
import pyarrow as pa

XLSX_FILE_PATH = 'src/data/BuyAmericanActExceptionsandWaiversOctober2023.xlsx'
CSV_FILE_PATH = 'src/data/FY2023_archived_opportunities.csv'
PARQUET_FILE_PATH = 'src/data/sample_contract_df.parquet'
DB_FILE_PATH = 'gov-contracts.db'
TABLE_NAME = 'FY2023_archived_opportunities'


def remove_columns_with_missing_data(df, threshold=0.5):
    """Removes columns from a DataFrame if they are missing more than a certain percentage of their observations."""
    missing_data_ratio = df.isnull().sum() / len(df)
    columns_to_keep = missing_data_ratio[missing_data_ratio <= threshold].index
    return df[columns_to_keep]

def convert_csv_to_parquet(csv_file_path, parquet_file_path):
    """Converts a CSV file to Parquet format."""
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
        df['Award$'] = pd.to_numeric(df['Award$'], errors='coerce')
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace('/', '_').str.replace('-', '_').str.replace('#', '').str.replace('$', '')
        df = df[['department_ind_agency', 'cgac', 'sub_tier',
                'fpds_code', 'office', 'aac_code', 'posteddate', 'type', 'basetype',
                'popstreetaddress', 'popcity', 'popstate', 'popzip', 'popcountry',
                'active', 'awardnumber', 'awarddate', 'award', 'awardee',
                'state', 'city', 'zipcode', 'countrycode']]
        #df = remove_columns_with_missing_data(df)

        # department_ind_agency: Replace ", DEPARTMENT OF" with ""
        

        df.to_parquet(parquet_file_path, index=False)
    except Exception as e:
        print(f"Error converting CSV to Parquet: {e}")

def load_parquet_to_sqlite(parquet_file_path, db_file_path, table_name):
    """Loads a Parquet file into a SQLite database."""
    try:
        df = pd.read_parquet(parquet_file_path)
        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error loading Parquet file into SQLite: {e}")

def load_xlsx_to_sqlite(xlsx_file_path, db_file_path, table_name):
    """Loads an XLSX file into a SQLite database."""
    try:
        df = pd.read_excel(xlsx_file_path, skiprows=1, header=0)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        df = remove_columns_with_missing_data(df)

        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error loading XLSX file into SQLite: {e}")


# Clear all data from SQLite database
# with sqlite3.connect(DB_FILE_PATH) as conn:
#     conn.execute("DELETE FROM ContractOpportunitiesFull")

# Convert CSV to Parquet
# Load the file from CSV_FILE_PATH and show a simple summary statistics 
df = pd.read_csv(CSV_FILE_PATH, encoding='ISO-8859-1')
df['Award$'] = pd.to_numeric(df['Award$'], errors='coerce')
df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace('/', '_').str.replace('-', '_').str.replace('#', '')
# Convert posteddate from datetime to date 

#df = remove_columns_with_missing_data(df)
print(df.columns)

convert_csv_to_parquet(CSV_FILE_PATH, PARQUET_FILE_PATH)

# Load Parquet into SQLite
load_parquet_to_sqlite(PARQUET_FILE_PATH, DB_FILE_PATH, TABLE_NAME)
# Load XLSX into SQLite
#load_xlsx_to_sqlite(XLSX_FILE_PATH, DB_FILE_PATH, TABLE_NAME)
