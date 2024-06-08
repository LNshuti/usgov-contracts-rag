
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

results = defog.run_query(
    "how many from San Francisco",
    previous_context=results['previous_context']
)
{
    'columns': ['num_users'],
    'data': [(50,)],
    'query_generated': "SELECT COUNT(*) AS num_users FROM users WHERE city ILIKE '%San Francisco%';",
    'ran_successfully': True,
    'reason_for_query': "The user is asking for the number of users from San Francisco. The city of the user is stored in the 'city' column of the 'users' table. Therefore, we can use a simple COUNT query to count the number of users from San Francisco. We will use the ILIKE operator to perform a case-insensitive match on the city name, as the user may have typed it in different ways. Since the query only requires one table, we do not need to use a JOIN statement. ",
    'previous_context': [
        'how many users do we have?',
        'SELECT COUNT(userid) AS num_users FROM users;',
        'how many from San Francisco?',
        "SELECT COUNT(*) AS num_users FROM users WHERE city ILIKE '%San Francisco%';"
    ]
}