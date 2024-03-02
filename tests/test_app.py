import unittest
import sqlite3
import pandas as pd
import streamlit as st
import pyperclip
import os
from app import StreamlitChatPack
from unittest.mock import patch, MagicMock

class TestStreamlitChatPack(unittest.TestCase):
    def setUp(self):
        self.app = StreamlitChatPack()

    # Database Interaction Tests
    def test_database_connection(self):
        engine = self.app.load_db_llm()[2]
        self.assertIsNotNone(engine.connect())

    def test_table_retrieval(self):
        engine = self.app.load_db_llm()[2]
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        self.assertIsInstance(tables, list)

    def test_data_retrieval(self):
        engine = self.app.load_db_llm()[2]
        with engine.connect() as conn:
            data = self.app.get_table_data('table_name', conn)
        self.assertIsInstance(data, pd.DataFrame)

    # User Input Handling Tests
    def test_session_state_initialization(self):
        self.app.run()  # This is to simulate starting the app
        self.assertIn("messages", st.session_state)

    def test_chat_history_update(self):
        self.app.run()  # Start the app
        test_message = {"role": "user", "content": "test message"}
        self.app.add_to_message_history(test_message["role"], test_message["content"])
        self.assertIn(test_message, st.session_state["messages"])

    # Natural Language to SQL Query Conversion Tests
    def test_query_generation(self):
        with patch('app.OpenAI_API_Call', return_value='expected SQL query') as mock_api_call:
            query = self.app.generate_query('natural language input')
            mock_api_call.assert_called_once_with('natural language input')
            self.assertEqual(query, 'expected SQL query')

    # Clipboard Functionality Tests
    def test_clipboard_copy(self):
        test_prompt = "Test prompt"
        with patch('app.pyperclip.copy') as mock_copy:
            self.app.copy_prompt_to_clipboard(test_prompt)
            mock_copy.assert_called_once_with(test_prompt)

if __name__ == '__main__':
    unittest.main()
