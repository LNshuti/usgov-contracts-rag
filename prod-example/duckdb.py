import duckdb
duckdb.read_csv("../data/ContractOpportunitiesFull.csv")

duckdb.sql("SELECT * FROM ContractOpportunitiesFull LIMIT 10;")

# Add main 
