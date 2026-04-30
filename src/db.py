import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="postgres_toolkit",
        port=5432
    )
