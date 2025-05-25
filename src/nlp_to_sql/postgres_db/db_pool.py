import os
from psycopg2 import pool
from src.chatBot_app.utils import setup_logger

logger = setup_logger(__name__)

class PostgresPool:
    def __init__(self):
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            database=os.getenv('POSTGRES_DB', 'postgres'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'qwerty'),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
        )
        logger.info('PostgreSQL connection pool created')

    def get_conn(self):
        return self.pool.getconn()

    def put_conn(self, conn):
        self.pool.putconn(conn)

    def closeall(self):
        self.pool.closeall()

# Singleton instance
postgres_pool = PostgresPool()
