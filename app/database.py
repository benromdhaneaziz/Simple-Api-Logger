import sqlite3

DATABASE = "logs.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            method TEXT,
            path TEXT,
            request_body TEXT,
            status_code INTEGER,
            response_time REAL
        )
    ''')
    conn.commit()
    conn.close()
