import os
from psycopg2 import pool
from src.chatBot_app.utils import setup_logger
from src.config import Config

logger = setup_logger(__name__)

class PostgresPool:
    def __init__(self):
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            database=Config.POSTGRES_DB,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            host=Config.POSTGRES_HOST,
            port=Config.POSTGRES_PORT if Config.POSTGRES_PORT else 5432,  # Default PostgreSQL port
        )
        logger.info('PostgreSQL connection pool created')

    def get_conn(self):
        return self.pool.getconn()

    def put_conn(self, conn):
        self.pool.putconn(conn)

    def closeall(self):
        self.pool.closeall()

# Singleton instance
POSTGRES_POOL = PostgresPool()
