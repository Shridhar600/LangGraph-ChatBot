from .db_pool import postgres_pool
from src.chatBot_app.utils import setup_logger

logger = setup_logger(__name__)

def test_connection():
    conn = None
    try:
        conn = postgres_pool.get_conn()
        with conn.cursor() as cur:
            cur.execute('SELECT 1')
            logger.info('Database connected successfully')
            print('Database connected successfully')
    except Exception as e:
        logger.exception('Database not connected successfully')
        print(f'Database not connected successfully: {e}')
    finally:
        if conn:
            postgres_pool.put_conn(conn)
