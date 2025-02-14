import sqlite3

# Name of the database file
DATABASE = "logs.db"

def create_schema():
    conn = sqlite3.connect(DATABASE)
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
    print("Database schema created successfully.")

if __name__ == '__main__':
    create_schema()
