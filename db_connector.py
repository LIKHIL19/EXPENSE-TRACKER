import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Likhil@1976",
        database="price_comparison"
    )
