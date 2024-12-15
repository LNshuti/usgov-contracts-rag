import sqlite3
import pandas as pd
import openpyxl 
import pyarrow as pa
from sklearn.impute import SimpleImputer

XLSX_FILE_PATH = 'src/data/BuyAmericanActExceptionsandWaiversOctober2023.xlsx'
CSV_FILE_PATH = 'src/data/FY2023_archived_opportunities.csv'
PARQUET_FILE_PATH = 'src/data/sample_contract_df.parquet'
DB_FILE_PATH = 'gov-contracts.db'
TABLE_NAME = 'FY2023_archived_opportunities'


def remove_columns_with_missing_data(df, threshold=0.3):
    """Removes columns from a DataFrame if they are missing more than a certain percentage of their observations."""
    missing_data_ratio = df.isnull().sum() / len(df)
    columns_to_keep = missing_data_ratio[missing_data_ratio <= threshold].index
    return df[columns_to_keep]

def impute_missing_values(df):
    """Impute missing values in the DataFrame. Numeric columns are imputed with mean, 
    and non-numeric columns are imputed with the most frequent value."""
    # Separate numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    non_numeric_cols = df.select_dtypes(exclude=['number']).columns

    # Impute numeric columns with mean
    if len(numeric_cols) > 0:
        imputer_num = SimpleImputer(strategy='mean')
        df[numeric_cols] = imputer_num.fit_transform(df[numeric_cols])

    # Impute non-numeric columns with most frequent value
    if len(non_numeric_cols) > 0:
        imputer_cat = SimpleImputer(strategy='most_frequent')
        df[non_numeric_cols] = imputer_cat.fit_transform(df[non_numeric_cols])
    
    return df

def convert_csv_to_parquet(csv_file_path, parquet_file_path):
    """Converts a CSV file to Parquet format with cleaning and imputation."""
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
        df['Award$'] = pd.to_numeric(df['Award$'], errors='coerce')
        df.columns = (df.columns
                        .str.lower()
                        .str.replace(' ', '_')
                        .str.replace('.', '_')
                        .str.replace('/', '_')
                        .str.replace('-', '_')
                        .str.replace('#', '')
                        .str.replace('$', ''))
        
        # Keep only desired columns as per the original script
        df = df[['department_ind_agency', 'cgac', 'sub_tier',
                 'fpds_code', 'office', 'aac_code', 'posteddate', 'type', 'basetype',
                 'popstreetaddress', 'popcity', 'popstate', 'popzip', 'popcountry',
                 'active', 'awardnumber', 'awarddate', 'award', 'awardee',
                 'state', 'city', 'zipcode', 'countrycode']]

        # Remove columns with more than 30% missing data
        df = remove_columns_with_missing_data(df, threshold=0.3)

        # Impute missing values in the remaining columns
        df = impute_missing_values(df)

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
    """Loads an XLSX file into a SQLite database with cleaning and imputation."""
    try:
        df = pd.read_excel(xlsx_file_path, skiprows=1, header=0)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Remove columns with more than 30% missing data
        df = remove_columns_with_missing_data(df, threshold=0.3)

        # Impute missing values
        df = impute_missing_values(df)

        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error loading XLSX file into SQLite: {e}")


# Example usage:
# Clear all data from SQLite database if needed
# with sqlite3.connect(DB_FILE_PATH) as conn:
#     conn.execute("DELETE FROM ContractOpportunitiesFull")

# Check columns before processing
df = pd.read_csv(CSV_FILE_PATH, encoding='ISO-8859-1')
df['Award$'] = pd.to_numeric(df['Award$'], errors='coerce')
df.columns = (df.columns
                .str.lower()
                .str.replace(' ', '_')
                .str.replace('.', '_')
                .str.replace('/', '_')
                .str.replace('-', '_')
                .str.replace('#', '')
                .str.replace('$', ''))

print("Columns before processing:", df.columns)

# Convert CSV to Parquet with imputation
convert_csv_to_parquet(CSV_FILE_PATH, PARQUET_FILE_PATH)

# Load Parquet into SQLite
load_parquet_to_sqlite(PARQUET_FILE_PATH, DB_FILE_PATH, TABLE_NAME)

# If desired, load XLSX into SQLite
# load_xlsx_to_sqlite(XLSX_FILE_PATH, DB_FILE_PATH, TABLE_NAME)
