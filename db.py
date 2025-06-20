import sqlite3

def get_db_connection():
    conn = sqlite3.connect('paradigma.db')
    conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
    return conn
