import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import app  # Ensure app.py and test_app.py are in the same directory

class TestAppFunctions(unittest.TestCase):
    # Existing tests...

    @patch('app.execute_sql_query')
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
            'posteddate': ['2023-01-01', '2023-01-02'],
            'award': [1000.0, 2000.0],
            'awardee': ['Awardee1', 'Awardee2'],
            'state': ['State1', 'State2'],
            'city': ['City1', 'City2'],
            'zipcode': ['123456789', '987654321'],
            'zip': ['12345', '98765']
        })
        mock_execute_sql_query.return_value = (mock_df, "")

        sql_query, error, result_df, exec_error = app.handle_example_click(example_query)

        self.assertEqual(sql_query.strip(), expected_sql_query.strip())
        self.assertEqual(error, "")
        pd.testing.assert_frame_equal(result_df, mock_df)
        self.assertEqual(exec_error, "")

        mock_openai.assert_called_once()
        mock_execute_sql_query.assert_called_once_with(expected_sql_query.strip())

if __name__ == '__main__':
    unittest.main()
