# Retrieval Augmented Generation Text-to-SQL Application To Analyze US Government Contract Data

This python [application](https://leoncensh-usgov-contracts-rag.hf.space) uses Retrieval Augmented Generation(RAG) to ask the data questions directly using plain English. The application then uses OPENAI's GPT 4.o-mini model to convert this question i.e prompt into SQL, which then queries the DuckDb database that stores the data and returns the solution, *in addition to the SQL statement that generates this data*. 

The simplicity of testing the correctness of the answers makes this application a powerful, and useful use of Large Language Models(LLMs) in Data Science that can directly provide values to Business Users who are unfamiliar with SQL by allowing them to directly use Business Questions to answer Data Questions in seconds with a Gradio Application.    

# Demo 
https://www.loom.com/share/f292263472ae4e9cbfa813655bc7c654?sid=c3a5bf89-f80f-4d69-bae0-79beee641cbe

## Customize this Application with your own Data

### Clone this Repository

```bash
git clone https://github.com/LNshuti/usgov-contracts-rag.git
```

### Setup your Environment
```bash
conda env create --file=environment.yaml
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

### Update path in the connect_db.py file to load your Excel/CSV data into the database

```bash
CSV_FILE_PATH = 'data/your_data.csv'
DB_FILE_PATH = 'gov-contracts.db'
TABLE_NAME = 'your_table_name'
```

### Run the **connect_db.py** python helper file to load your data into the database
```bash
python connect_db.py
```

### Examine the data with Datasette
```bash
datasette serve gov-contracts.db
```

### Run the **app.py** python file to start the Gradio Application
```bash
python run app/app.py
```
**If you found the app useful, please make sure to give us a star!**

<img width="185" alt="Starred" src="https://github.com/mishushakov/llm-scraper/assets/10400064/11e2a79f-a835-48c4-9f85-5c104ca7bb49">

### References. 
1. Harshad Suryawanshi. From Natural Language to SQL(Na2SQL): Extracting Insights from Databases using OPENAI GPT3.5 and LlamaIndex. https://github.com/AI-ANK/Na2SQL

2. Ravi Theja. Evaluate RAG with Llamaindex. https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex
   
3. Mostafa Ibrahim. A Gentle Introduction to Advanced RAG. https://wandb.ai/mostafaibrahim17/ml-articles/reports/A-Gentle-Introduction-to-Advanced-RAG--Vmlldzo2NjIyNTQw
   
4. Adam Obeng; J.C. Zhong; Charlie Gu. How we built Text-to-SQL at Pinterest. https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff
   
