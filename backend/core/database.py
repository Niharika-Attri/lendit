import psycopg2
from psycopg2.extras import RealDictCursor
import time

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="lendit",
                user="postgres",
                password="Na123@2005",
                cursor_factory=RealDictCursor
            )
            cursor = conn.cursor()
            print("Database connected successfully")
            return conn, cursor
        except Exception as error:
            print(f"Database connection failed: {error}")
            time.sleep(2)

conn, cursor = get_db_connection()