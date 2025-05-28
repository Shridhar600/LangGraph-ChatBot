from src.nlp_to_sql import POSTGRES_POOL
from langchain_core.tools import tool
from src.chatBot_app import setup_logger
log = setup_logger(__name__)

@tool(name_or_callable ="execute_sql_query", description="Executes a SQL query on user's PostgresSQL database.")
def execute_sql_query(query):
    """
    Executes a SQL query on user's PostgresSQL database.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list: A list of tuples containing the results of the query.
    """
    log.info(f"AI Requested SQL query: {query}")
    try:
        conn = POSTGRES_POOL.get_conn()
        with conn.cursor() as cur:
            cur.execute(query)
            results = cur.fetchall()
            log.info('Database query executed successfully')
            return (f'Query executed successfully. Results: {results}', results)
    except Exception as e:
        log.warning(f'Database query execution failed: {e}')
        return f"Error executing query: {e}"
    finally:
        if conn:
            POSTGRES_POOL.put_conn(conn)