import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Likhil@1976",
    "database": "expense_tracker"
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise RuntimeError(f"Database connection failed: {e}")

def execute_query(query, params=None, fetchone=False, fetchall=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()
