# src/tests/test_app.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from app import app  # Ensure correct import path

class TestAppFunctions(unittest.TestCase):
    # Existing tests...

    @patch('src.app.app.execute_sql_query')
    @patch('openai.ChatCompletion.create')
    def test_handle_example_click_with_custom_query(self, mock_openai, mock_execute_sql_query):
        # Example natural language query
        example_query = ("Select the first five characters of zipcode named zip as a separate column "
                         "SELECT department_ind_agency, cgac, fpds_code, office, aac_code, posteddate, "
                         "award, awardee, state, city, zipcode FROM contract_data WHERE basetype = 'Award Notice' "
                         "AND LENGTH(awardee) >= 10 AND LENGTH(popcity) > 5 LIMIT 15")

        # Expected SQL query
        expected_sql_query = '''
        SELECT
            department_ind_agency,
            cgac,
            fpds_code,
            office,
            aac_code,
            posteddate,
            award,
            awardee,
            state,
            city,
            zipcode,
            LEFT(zipcode, 5) AS zip
        FROM contract_data
        WHERE
            basetype = 'Award Notice' AND
            LENGTH(awardee) >= 10 AND
            LENGTH(popcity) > 5
        LIMIT 15;
        '''

        # Mock OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=expected_sql_query))]
        mock_openai.return_value = mock_response

        # Mock execute_sql_query response
        mock_df = pd.DataFrame({
            'department_ind_agency': ['Dept1', 'Dept2'],
            'cgac': [123, 456],
            'fpds_code': ['FP1', 'FP2'],
            'office': ['Office1', 'Office2'],
            'aac_code': ['AAC1', 'AAC2'],
            'posteddate': ['2021-01-01', '2021-01-02'],
            'award': ['Award1', 'Award2'],
            'awardee': ['Awardee1', 'Awardee2'],
            'state': ['State1', 'State2'],
            'city': ['City1', 'City2'],
            'zipcode': ['12345', '67890'],
            'zip': ['12345', '67890']
        })
        mock_execute_sql_query.return_value = mock_df

        # Call the function to test
        result = app.handle_example_click(example_query)

        # Assert the result
        pd.testing.assert_frame_equal(result, mock_df)
        
