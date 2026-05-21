from psycopg2 import pool
import os

from dotenv import load_dotenv
from src.utils import config

load_dotenv() # reads the .env file and loads all variables


connection_pool = pool.SimpleConnectionPool(
    1, # min connections
    10, # max connections
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "postgres_toolkit"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

def get_connection():
    return connection_pool.getconn()
