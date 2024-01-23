import streamlit as st
import pyperclip
#import wandb 

#from st_aggrid import AgGrid
from sqlalchemy import create_engine, inspect, text
from typing import Dict, Any

from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.llms import OpenAI
import openai
import os
import pandas as pd

from llama_index.llms.palm import PaLM

from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
import sqlite3

from llama_index import SQLDatabase, ServiceContext
from llama_index.indices.struct_store import NLSQLTableQueryEngine

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']


class StreamlitChatPack(BaseLlamaPack):

    def __init__(
        self,
        page: str = "Natural Language to SQL Query",
        run_from_main: bool = False,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        
        self.page = page

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}
    
    def copy_prompt_to_clipboard(self, prompt):
        pyperclip.copy(prompt)
        st.success("Copied to clipboard!")

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import streamlit as st
        # Initialize Weights & Biases
        #wandb.init(project='streamlit-chat-app', entity='leoncen0-iga')


        st.set_page_config(
            page_title=f"{self.page}",
            layout="centered",
            initial_sidebar_state="auto",
            menu_items=None,
        )

        if "messages" not in st.session_state:  # Initialize the chat messages history
            st.session_state["messages"] = [
                {"role": "assistant", "content": f"#### Ask a custom question about the data in the database."}
            ]

        st.title(
            f"{self.page}🇺🇸"
        )
        st.info(
            f"Pose any question about the selected table and receive exact SQL queries."
        )

        def add_to_message_history(role, content):
            message = {"role": role, "content": str(content)}
            st.session_state["messages"].append(
                message
            )  # Add response to message history

        def get_table_data(table_name, conn):
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            return df

        @st.cache_resource
        def load_db_llm():
            # Load the SQLite database
            engine = create_engine("sqlite:///gov-contracts.db")
            sql_database = SQLDatabase(engine) #include all tables

            # Initialize LLM
            llm2 = OpenAI(temperature=0.1, model="gpt-3.5-turbo-1106")

            service_context = ServiceContext.from_defaults(llm=llm2, embed_model="local")
            
            return sql_database, service_context, engine

        sql_database, service_context, engine = load_db_llm()


       # Sidebar for database schema viewer
        st.sidebar.markdown("## Database Schema Viewer")

        # Create an inspector object
        inspector = inspect(engine)

        # Get list of tables in the database
        table_names = inspector.get_table_names()

        # Sidebar selection for tables
        selected_table = st.sidebar.selectbox("Select a Table", table_names)

        db_file = 'gov-contracts.db'
        conn = sqlite3.connect(db_file)
    
        # Display the selected table
        if selected_table:
            # Log the table selection event
            #wandb.log({"selected_table": selected_table})
            df = get_table_data(selected_table, conn)
            st.sidebar.text(f"Data for table '{selected_table}':")
            st.sidebar.dataframe(df)
            #AgGrid(df)
            #st.dataframe(df)

            # Show the column names and their types. Include in main panel and not on sidebar
            st.markdown("#### Table Schema")
    
            columns = inspector.get_columns(selected_table)
            data = [{"Feature": column['name'], "Data Type": str(column['type'])} for column in columns]
            df = pd.DataFrame(data)
            
            st.table(df)
            # columns = inspector.get_columns(selected_table)
            # for column in columns:
            #     st.markdown(f"**{column['name']}** ({column['type']})")
            
            # Add streamlit text telling the user to select an example prompt: 
            st.markdown("#### Select From Example Prompts")
            example_prompts = ["Return the department_ind_agency and the sum of award in descending order", 
                               "Return the sum of award in descending order grouped by type limited to the top 10"]

            for prompt in example_prompts:
                if st.button(prompt):
                    selected_prompt = prompt
                    # Log the selected prompt
                    #wandb.log({"selected_prompt": prompt})
                    break
            else:
                selected_prompt = None
    
        # Close the connection
        conn.close()
                
        # Sidebar Intro
        st.sidebar.markdown('## App Created By')
        st.sidebar.markdown("""
        Leonce Nshuti: 
        [Linkedin](https://www.linkedin.com/in/leoncenshuti/), [Github](https://github.com/LNshuti), [X](https://twitter.com/LeonceNshuti)
        """)
        st.sidebar.markdown('Inspired by Harshad Suryawanshi [Ecommerce RAG Demo](https://github.com/LNshuti/Na2SQL)')
    
        
        st.sidebar.markdown('## Other Projects')
        st.sidebar.markdown("""
        - [GRE AI Studdy Buddy: AI Agent to Manage Preparing for the GRE](https://github.com/LNshuti/gre-ai-buddy)
        - [Tennessee Eviction Tracker](https://github.com/LNshuti/evictions-dashboard)
        """)
        
        if "query_engine" not in st.session_state:  # Initialize the query engine
            st.session_state["query_engine"] = NLSQLTableQueryEngine(
                sql_database=sql_database,
                synthesize_response=True,
                service_context=service_context
            )

        for message in st.session_state["messages"]:  # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])


        if prompt := st.chat_input(
            "Enter your natural language query about the database"
        ):  # Prompt for user input and save to chat history
             # Log the user query
            #wandb.log({"user_query": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            add_to_message_history("user", prompt)

        if selected_prompt and (not st.session_state["messages"] or st.session_state["messages"][-1]["content"] != selected_prompt):
            with st.chat_message("user"):
                st.write(selected_prompt)
                add_to_message_history("user", selected_prompt)

            with st.spinner():
                with st.chat_message("assistant"):
                    response = st.session_state["query_engine"].query("User Question:"+selected_prompt+". ")
                    sql_query = f"```sql\n{response.metadata['sql_query']}\n```\n**Response:**\n{response.response}\n"
                    response_container = st.empty()
                    # Add copy to clipboard functionality
                    copy_button = st.button("Copy", key="copy_user")
                    if copy_button:
                        st.session_state["clipboard_content"] = sql_query
                        st.experimental_set_query_params(clipboard=st.session_state["clipboard_content"])
                        st.success("Copied to clipboard!")
                    response_container.write(sql_query)
                    add_to_message_history("assistant", sql_query)

        # If last message is not from assistant, generate a new response
        if st.session_state["messages"][-1]["role"] != "assistant":
            with st.spinner():
                with st.chat_message("assistant"):
                    response = st.session_state["query_engine"].query("User Question:"+prompt+". ")
                    sql_query = f"```sql\n{response.metadata['sql_query']}\n```\n**Response:**\n{response.response}\n"
                    response_container = st.empty()
                    # Add copy to clipboard functionality
                    copy_button = st.button("Copy", key="copy_assistant")
                    if copy_button:
                        st.session_state["clipboard_content"] = sql_query
                        st.experimental_set_query_params(clipboard=st.session_state["clipboard_content"])
                        st.success("Copied to clipboard!")
                    response_container.write(sql_query)
                    add_to_message_history("assistant", sql_query)
    #wandb.finish()
    
if __name__ == "__main__":
    StreamlitChatPack(run_from_main=True).run()
