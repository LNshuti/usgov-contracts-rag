# Retrieval Augmented Generation Text-to-SQL Application To Analyze US Government Contract Data

This python [application](https://usgov-contracts-analysis-rag.streamlit.app/) uses Retrieval Augmented Generation(RAG) to ask the data questions directly using plain English. The application then uses OPENAI's GPT 3.5 model to convert this question i.e prompt into SQL, which then queries the SQL Alchemy database that stores the data and returns the solution, *in addition to the SQL statement that generates this data*. 

The simplicity of testing the correctness of the answers makes this application a powerful, and useful use of Large Language Models(LLMs) in Data Science that can directly provide values to Business Users who are unfamiliar with SQL by allowing them to directly use Business Questions to answer Data Questions in seconds with a Streamlit Application.    

# Demo 
https://www.loom.com/share/f292263472ae4e9cbfa813655bc7c654?sid=c3a5bf89-f80f-4d69-bae0-79beee641cbe

## Customize this Application with your own Data

### Clone this Repository

```bash
git clone https://github.com/LNshuti/usgov-contracts-rag.git
```

### Setup your Environment
```bash
conda env create -f environment.yml
```

### Activate your Environment
```bash
conda activate gov-data
```

### Install Dependencies
```bash 
pip install -r requirements.txt
```

### Add your data in the data folder
```bash
cd data

cp <your_data> .
```

### Update path in the connect_db file to load your Excel/CSV data into the database

```bash
XLSX_FILE_PATH = 'data/BuyAmericanActExceptionsandWaiversOctober2023.xlsx'
CSV_FILE_PATH = 'data/contract_subset.csv'
PARQUET_FILE_PATH = 'data/sample_contract_df.parquet'
DB_FILE_PATH = 'gov-contracts.db'
TABLE_NAME = 'table_name'
```

### Run the **connect_db.py** python helper file to load your data into the database
```bash
python connect_db.py
```

### Run the **app.py** python file to start the Streamlit Application
```bash
streamlit run text-to-sql-rag/app.py
```

### References. 
1. Harshad Suryawanshi. From Natural Language to SQL(Na2SQL): Extracting Insights from Databases using OPENAI GPT3.5 and LlamaIndex. https://github.com/AI-ANK/Na2SQL

2. Ravi Theja. Evaluate RAG with Llamaindex. https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex
