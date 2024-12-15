# Retrieval Augmented Generation Text-to-SQL Application To Analyze US Government Contract Data

This python [application](https://leoncensh-usgov-contracts-rag.hf.space) uses Retrieval Augmented Generation(RAG) to ask the data questions directly using plain English. The application then uses OPENAI's GPT 4.o-mini model to convert this question i.e prompt into SQL, which then queries the DuckDb database that stores the data and returns the solution, *in addition to the SQL statement that generates this data*. 

The simplicity of testing the correctness of the answers makes this application a powerful, and useful use of Large Language Models(LLMs) in Data Science that can directly provide values to Business Users who are unfamiliar with SQL by allowing them to directly use Business Questions to answer Data Questions in seconds with a Gradio Application.    

# Demo 
![usgovrag480](https://github.com/user-attachments/assets/6097a787-f4be-4b00-82e6-f18542ecdfb8)



## Customize this Application with your own Data

**If you found the app useful, please make sure to give us a star!**

![image](https://github.com/user-attachments/assets/4063a746-4bc9-4f30-ae53-de212d6e3b1e)

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

### Enhancement: XGBOOST prediction of government contract awards with confidence intervals
In addition to the previous work exploring the dataset, I've developed an appliction using the same dataset to predict award amounts based on the other features. 
This app has a gradio interface, and it's built in python, hosted on Huggingface. The app takes the dataset as an input to a gradient boosted tree model, after feature
engineering. The user can select a combination of the features to produce the predicted award amount with a 95% confidence interval based on the bootstrap method. 

#### [application](https://leoncensh-xgboost-gov-contracts.hf.space)


### References. 
1. Harshad Suryawanshi. From Natural Language to SQL(Na2SQL): Extracting Insights from Databases using OPENAI GPT3.5 and LlamaIndex. https://github.com/AI-ANK/Na2SQL

2. Ravi Theja. Evaluate RAG with Llamaindex. https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex
   
3. Mostafa Ibrahim. A Gentle Introduction to Advanced RAG. https://wandb.ai/mostafaibrahim17/ml-articles/reports/A-Gentle-Introduction-to-Advanced-RAG--Vmlldzo2NjIyNTQw
   
4. Adam Obeng; J.C. Zhong; Charlie Gu. How we built Text-to-SQL at Pinterest. https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff
   
