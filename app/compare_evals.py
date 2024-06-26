
from defog import Defog
import os 

api_key = os.getenv("DEFOG_API_KEY")
db_type = os.getenv("DB_TYPE")
db_creds = os.getenv("YOUR_DB_CREDS")

defog = Defog(
    api_key = "YOUR_DEFOG_API_KEY",
    db_type = "YOUR_DB_TYPE",
    # must be one of postgres, redshift, mysql, snowflake, or bigquery
    db_creds = "YOUR_DB_CREDS"
    # must be a dict in these formats, depending
    # on your database type
    # https://github.com/defog-ai/defog-python/blob/63af5e3ded07da356365f20bc94a194c4f7c44fa/defog/__init__.py#L110
)

results = defog.run_query("how many from San Francisco")
previous_context=results['previous_context']

defog.update_glossary("""- If a user asks for data in this week, return data for the current ISO week and not for the last 7 days.
- CAC refers to the Customer Acquisition cost, and can be compute by ...""")