import sqlite3
import pandas as pd
import pyarrow as pa

CSV_FILE_PATH = 'data/contract_subset.csv'
PARQUET_FILE_PATH = 'data/sample_contract_df.parquet'
DB_FILE_PATH = 'gov-contracts.db'
TABLE_NAME = 'table_name'

def remove_columns_with_missing_data(df, threshold=0.05):
    """Removes columns from a DataFrame if they are missing more than a certain percentage of their observations."""
    missing_data_ratio = df.isnull().sum() / len(df)
    columns_to_keep = missing_data_ratio[missing_data_ratio <= threshold].index
    return df[columns_to_keep]

def convert_csv_to_parquet(csv_file_path, parquet_file_path):
    """Converts a CSV file to Parquet format."""
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
        df['Award$'] = pd.to_numeric(df['Award$'], errors='coerce')
        df = remove_columns_with_missing_data(df)

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

# Convert CSV to Parquet
convert_csv_to_parquet(CSV_FILE_PATH, PARQUET_FILE_PATH)

# Load Parquet into SQLite
load_parquet_to_sqlite(PARQUET_FILE_PATH, DB_FILE_PATH, TABLE_NAME)