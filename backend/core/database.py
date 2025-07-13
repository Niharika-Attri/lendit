import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Depends
from core.config import config

def get_db():
    conn = psycopg2.connect(
        host="localhost",
        database=config['DATABASE'],
        user="postgres",
        password=config['POSTGRES_PASSWORD'],
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()