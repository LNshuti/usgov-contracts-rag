import json
import openai
import gradio as gr
import duckdb
from functools import lru_cache
import os

from fastapi import FastAPI
import uvicorn

# =========================
# Configuration and Setup
# =========================

openai.api_key = os.getenv("OPENAI_API_KEY")
dataset_path = 'data/sample_contract_df.parquet'  

schema = [
    {"column_name": "department_ind_agency", "column_type": "VARCHAR"},
    {"column_name": "cgac", "column_type": "BIGINT"},
    {"column_name": "sub_tier", "column_type": "VARCHAR"},
    {"column_name": "fpds_code", "column_type": "VARCHAR"},
    {"column_name": "office", "column_type": "VARCHAR"},
    {"column_name": "aac_code", "column_type": "VARCHAR"},
    {"column_name": "posteddate", "column_type": "VARCHAR"},
    {"column_name": "type", "column_type": "VARCHAR"},
    {"column_name": "basetype", "column_type": "VARCHAR"},
    {"column_name": "popstreetaddress", "column_type": "VARCHAR"},
    {"column_name": "popcity", "column_type": "VARCHAR"},
    {"column_name": "popstate", "column_type": "VARCHAR"},
    {"column_name": "popzip", "column_type": "VARCHAR"},
    {"column_name": "popcountry", "column_type": "VARCHAR"},
    {"column_name": "active", "column_type": "VARCHAR"},
    {"column_name": "awardnumber", "column_type": "VARCHAR"},
    {"column_name": "awarddate", "column_type": "VARCHAR"},
    {"column_name": "award", "column_type": "DOUBLE"},
    {"column_name": "awardee", "column_type": "VARCHAR"},
    {"column_name": "state", "column_type": "VARCHAR"},
    {"column_name": "city", "column_type": "VARCHAR"},
    {"column_name": "zipcode", "column_type": "VARCHAR"},
    {"column_name": "countrycode", "column_type": "VARCHAR"}
]

@lru_cache(maxsize=1)
def get_schema():
    return schema

COLUMN_TYPES = {col['column_name']: col['column_type'] for col in get_schema()}

# =========================
# OpenAI API Integration
# =========================

def parse_query(nl_query):
    messages = [
        {"role": "system", "content": "You are an assistant that converts natural language queries into SQL queries for the 'contract_data' table."},
        {"role": "user", "content": f"Schema:\n{json.dumps(schema, indent=2)}\n\nQuery:\n\"{nl_query}\"\n\nSQL:"}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=150,
        )
        sql_query = response.choices[0].message.content.strip()
        return sql_query, ""
    except Exception as e:
        return "", f"Error generating SQL query: {e}"

# =========================
# Database Interaction
# =========================

def execute_sql_query(sql_query):
    try:
        con = duckdb.connect()
        con.execute(f"CREATE OR REPLACE VIEW contract_data AS SELECT * FROM '{dataset_path}'")
        result_df = con.execute(sql_query).fetchdf()
        con.close()
        return result_df, ""
    except Exception as e:
        return None, f"Error executing query: {e}"

# =========================
# Gradio Application UI
# =========================

with gr.Blocks() as demo:
    gr.Markdown("""
    # Use Text to SQL to analyze US Government contract data

    ## Instructions

    ### 1. **Describe the data you want**: e.g., `Show awards over 1M in CA`
    ### 2. **Use Example Queries**: Click on any example query button below to execute.
    ### 3. **Generate SQL**: Or, enter your own query and click "Generate SQL" to see the SQL query.

    ## Example Queries
    """)

    with gr.Row():
        with gr.Column(scale=1):
    
            gr.Markdown("### Click on an example query:")
            with gr.Row():
                btn_example1 = gr.Button("Retrieve the top 15 records from contract_data where basetype is Award Notice, awardee has at least 12 characters, and popcity has more than 5 characters. Exclude the fields sub_tier, popzip, awardnumber, basetype, popstate, active, popcountry, type, countrycode, and popstreetaddress")
                btn_example2 = gr.Button("Show top 10 departments by award amount")
                btn_example3 = gr.Button("SELECT department_ind_agency, CONCAT('$', ROUND(SUM(award), 0)) AS sum_award FROM contract_data GROUP BY department_ind_agency ORDER BY SUM(award) DESC LIMIT 25")
                btn_example4 = gr.Button("Retrieve the top 15 records from contract_data where basetype is Award Notice, awardee has at least 12 characters, and popcity has more than 5 characters. Exclude the fields sub_tier, popzip, awardnumber, basetype, popstate, active, popcountry, type, countrycode, and popstreetaddress")
                btn_example5 = gr.Button("SELECT awardnumber,awarddate,award, office, department_ind_agency,awardee from contract_data WHERE awardee IS NOT NULL AND award IS NOT NULL AND popcity IS NOT NULL AND award > 100000000 LIMIT 10;")

            query_input = gr.Textbox(
                label="Your Query",
                placeholder='e.g., "What are the total awards over 1M in California?"',
                lines=1
            )

            btn_generate_sql = gr.Button("Generate SQL Query")
            sql_query_out = gr.Code(label="Generated SQL Query", language="sql")
            btn_execute_query = gr.Button("Execute Query")
            error_out = gr.Markdown("", visible=False)
        with gr.Column(scale=2):
            results_out = gr.Dataframe(label="Query Results", interactive=False)

    with gr.Tab("Dataset Schema"):
        gr.Markdown("### Dataset Schema")
        schema_display = gr.JSON(label="Schema", value=get_schema())

    # =========================
    # Event Functions
    # =========================

    def generate_sql(nl_query):
        sql_query, error = parse_query(nl_query)
        return sql_query, error

    def execute_query(sql_query):
        result_df, error = execute_sql_query(sql_query)
        return result_df, error

    def handle_example_click(example_query):
        if example_query.strip().upper().startswith("SELECT"):
            sql_query = example_query
            result_df, error = execute_sql_query(sql_query)
            return sql_query, "", result_df, error
        else:
            sql_query, error = parse_query(example_query)
            if error:
                return sql_query, error, None, error
            result_df, exec_error = execute_sql_query(sql_query)
            return sql_query, exec_error, result_df, exec_error

    # =========================
    # Button Click Event Handlers
    # =========================

    btn_generate_sql.click(
        fn=generate_sql,
        inputs=query_input,
        outputs=[sql_query_out, error_out]
    )

    btn_execute_query.click(
        fn=execute_query,
        inputs=sql_query_out,
        outputs=[results_out, error_out]
    )

    btn_example1.click(
        fn=lambda: handle_example_click("Retrieve the top 15 records from contract_data where basetype is Award Notice, awardee has at least 12 characters, and popcity has more than 5 characters. Exclude the fields sub_tier, popzip, awardnumber, basetype, popstate, active, popcountry, type, countrycode, and popstreetaddress"),
        outputs=[sql_query_out, error_out, results_out, error_out]
    )
    btn_example2.click(
        fn=lambda: handle_example_click("Show top 10 departments by award amount. Round to zero decimal places."),
        outputs=[sql_query_out, error_out, results_out, error_out]
    )
    btn_example3.click(
        fn=lambda: handle_example_click("SELECT department_ind_agency, CONCAT('$', ROUND(SUM(award), 0)) AS sum_award FROM contract_data GROUP BY department_ind_agency ORDER BY SUM(award) DESC LIMIT 25"),
        outputs=[sql_query_out, error_out, results_out, error_out]
    )
    btn_example4.click(
        fn=lambda: handle_example_click("Retrieve the top 15 records from contract_data where basetype is Award Notice, awardee has at least 12 characters, and popcity has more than 5 characters. Exclude the fields sub_tier, popzip, awardnumber, basetype, popstate, active, popcountry, type, countrycode, and popstreetaddress"),
        outputs=[sql_query_out, error_out, results_out, error_out]
    )
    btn_example5.click(
        fn=lambda: handle_example_click("SELECT awardnumber,awarddate,award, office, department_ind_agency,awardee from contract_data WHERE awardee IS NOT NULL AND award IS NOT NULL AND popcity IS NOT NULL AND award > 100000000 LIMIT 10;"),
        outputs=[sql_query_out, error_out, results_out, error_out]
    )

    

# Launch the Gradio App
demo.launch(share=True)
