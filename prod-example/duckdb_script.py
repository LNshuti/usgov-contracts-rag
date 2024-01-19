import duckdb
# Import csv file using pandas 
import pandas as pd
import streamlit as st
df = pd.read_csv("/Users/lnshuti/Desktop/portfolio/usgov-contracts-rag/data/ContractOpportunitiesFull.csv", encoding='ISO-8859-1')
st.write(df)

# Print column names 
print(df.columns)

# Display summary of Award$ column by Sub-Tier 
df.groupby('Sub-Tier').describe()['Award$']

st.write(df.groupby('Sub-Tier').describe()['Award$'])

# Display the top 10 contracts based on Award$ where 
# the Sub-Tier is the Agency For International Development

df[df['Sub-Tier'] == 'AGENCY FOR INT (................................................................................................................................................................................................................................................................................................................................................................................................................................................tim krebs ERNATIONAL DEVELOPMENT'].sort_values('Award$', ascending=False).head(10)

# Display a Table 
duckdb.sql("SELECT * FROM ContractOpportunitiesFull LIMIT 10;")

     