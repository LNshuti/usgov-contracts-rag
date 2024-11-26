import json
import openai
import gradio as gr
import duckdb
from functools import lru_cache
import os

# =========================
# Configuration and Setup
# =========================

openai.api_key = os.getenv("OPENAI_API_KEY")
dataset_path = '../data/sample_contract_df.parquet'  # Update with your Parquet file path

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
            model="gpt-4o-mini",
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

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    <h1 style="text-align:center;">📊 Text-to-SQL Contract Data Explorer</h1>
    <p style="text-align:center; font-size:1.2em;">Analyze US Government contract data using natural language queries.</p>
    """)
    
    with gr.Row():
        with gr.Column(scale=1, min_width=350):
            gr.Markdown("### 🔍 Enter Your Query")
            query_input = gr.Textbox(
                label="",
                placeholder='e.g., "What are the total awards over $1M in California?"',
                lines=2
            )

            btn_generate_sql = gr.Button("📝 Generate SQL Query", variant="primary")
            sql_query_out = gr.Code(label="🛠️ Generated SQL Query", language="sql")

            btn_execute_query = gr.Button("🚀 Execute Query", variant="secondary")
            error_out = gr.Markdown("", visible=False, elem_id="error_message")
            
            gr.Markdown("### 💡 Example Queries")
            with gr.Column():
                example_queries = [
                    "Show the top 10 departments by total award amount.",
                    "List contracts where the award amount exceeds $5,000,000.",
                    "Retrieve awards over $1M in California.",
                    "Find the top 5 awardees by number of contracts.",
                    "Display contracts awarded after 2020 in New York.",
                    "What is the total award amount by state?"
                ]
                example_buttons = []
                for i, query in enumerate(example_queries):
                    btn = gr.Button(query, variant="link", size="sm", interactive=True)
                    example_buttons.append(btn)
            
            with gr.Accordion("📄 Dataset Schema", open=False):
                gr.JSON(get_schema(), label="Schema")

        with gr.Column(scale=2):
            gr.Markdown("### 📊 Query Results")
            results_out = gr.DataFrame(label="", interactive=False, row_count=10)
            status_info = gr.Markdown("", visible=False, elem_id="status_info")

    # =========================
    # Event Functions
    # =========================

    def generate_sql(nl_query):
        if not nl_query.strip():
            return "", "⚠️ Please enter a natural language query."
        sql_query, error = parse_query(nl_query)
        if error:
            return "", f"❌ {error}"
        return sql_query, ""

    def execute_query(sql_query):
        if not sql_query.strip():
            return None, "⚠️ Please generate an SQL query first."
        result_df, error = execute_sql_query(sql_query)
        if error:
            return None, f"❌ {error}"
        if result_df.empty:
            return None, "ℹ️ The query returned no results."
        return result_df, ""

    def handle_example_click(example_query):
        sql_query, error = parse_query(example_query)
        if error:
            return "", f"❌ {error}", None
        result_df, exec_error = execute_sql_query(sql_query)
        if exec_error:
            return sql_query, f"❌ {exec_error}", None
        return sql_query, "", result_df

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

    # Assign click events to example buttons
    for btn, query in zip(example_buttons, example_queries):
        btn.click(
            fn=lambda q=query: handle_example_click(q),
            inputs=None,
            outputs=[sql_query_out, error_out, results_out]
        )

# Launch the Gradio App
demo.queue().launch(debug=True, share=True)
