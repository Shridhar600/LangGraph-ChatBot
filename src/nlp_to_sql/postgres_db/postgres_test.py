from .db_pool import POSTGRES_POOL
from src.chatBot_app.utils import setup_logger

logger = setup_logger(__name__)

def test_connection():
    conn = None
    try:
        conn = POSTGRES_POOL.get_conn()
        with conn.cursor() as cur:
            # cur.execute('SELECT * from public.employee LIMIT 1;')
            # # logger.info(cur.fetchone())
            # logger.info(cur.fetchall())
            logger.info('Database connected successfully')
    except Exception as e:
        logger.warning(f'Database not connected successfully: {e}')
    finally:
        if conn:
            POSTGRES_POOL.put_conn(conn)
