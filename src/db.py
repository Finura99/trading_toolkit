from psycopg2 import pool
import os

from dotenv import load_dotenv
from src.utils import config

load_dotenv() # reads the .env file and loads all variables

DB_USER = os.getenv("DB_USER") # get env variables from .env
DB_PASSWORD = os.getenv("DB_PASSWORD")




connection_pool = pool.SimpleConnectionPool(
    1, # minimum connections
    10, # maximum connections
    host=config["database"]["host"],
    user=DB_USER,
    password=DB_PASSWORD,
    database="postgres_toolkit",
    port=config["database"]["port"]
)

def get_connection():
    return connection_pool.getconn()
