from contextlib import contextmanager
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv() # reads the .env file and loads all variables

@contextmanager
def db_connection(): # owns the connection lifecycle
    conn = connection_pool.getconn()

    try:
        yield conn # generator ?
    finally:
        connection_pool.putconn(conn) # automatic clean up with the context manager...


connection_pool = pool.SimpleConnectionPool(
    1, # min connections
    10, # max connections
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "postgres_toolkit"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def check_db_connection() -> bool:
    conn = None

    try:
        with db_connection() as conn:
            with conn.cursor() as cursor: #.cursor is the tool for sql to amend the data
                cursor.execute("SELECT 1;")
                cursor.fetchone()

        return True
    
    except Exception:
        return False
    
    finally:
            connection_pool.putconn(conn) # just checking