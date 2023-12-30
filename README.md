# Retrieval Augmented Generation Text-to-SQL Application To Analyze US Government Contract Data

This python [application](https://usgov-contracts-analysis-rag.streamlit.app/) uses Retrieval Augmented Generation(RAG) to ask the data questions directly using plain English. The application then uses OPENAI's GPT 3.5 model to convert this question i.e prompt into SQL, which then queries the SQL Alchemy database that stores the data and returns the solution, *in addition to the SQL statement that generates this data*. 

The simplicity of testing the correctness of the answers makes this application a powerful, and useful use of Large Language Models(LLMs) in Data Science that can directly provide values to Business Users who are unfamiliar with SQL by allowing them to directly use Business Questions to answer Data Questions in seconds with a Streamlit Application.    

### References. 
1. Harshad Suryawanshi. From Natural Language to SQL(Na2SQL): Extracting Insights from Databases using OPENAI GPT3.5 and LlamaIndex. https://github.com/AI-ANK/Na2SQL