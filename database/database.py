import sqlite3
import os

def connect():
    """
    Connect to the database.
    """
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'dev.sqlite'))
    cursor = conn.cursor()
    return conn, cursor

def migrate():
    """
    Migrate the database.
    """
    print('Migrate database...')
    conn, cursor = connect()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            description TEXT,
            game TEXT NOT NULL,
            expired BOOLEAN NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()