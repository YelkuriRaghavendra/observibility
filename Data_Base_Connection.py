import psycopg2
from psycopg2 import sql
import pandas as pd
from config import DB_HOST, DB_USER, DB_PASSWORD

def get_connection():
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=5432
    )
    return conn

def fetch_data(query, params=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)
