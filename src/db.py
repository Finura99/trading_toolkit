import psycopg2
from src.utils import config

def get_connection():
    return psycopg2.connect(
        host=config["database"]["host"],
        user="admin",
        password="admin",
        database="postgres_toolkit",
        port=config["database"]["port"]
    )