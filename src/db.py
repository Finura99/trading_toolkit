import psycopg2
import os

from dotenv import load_dotenv
from src.utils import config

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



def get_connection():
    return psycopg2.connect(
        host=config["database"]["host"],
        user=DB_USER,
        password=DB_PASSWORD,
        database="postgres_toolkit",
        port=config["database"]["port"]
    )