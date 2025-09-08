import sqlite3
import os

from dotenv import load_dotenv

from config.environments import Environment
from helpers.log import Log

def connect():
    """
    Connect to the database.
    """

    db_filename = 'dev.sqlite'

    if (os.getenv('ENVIRONMENT') == Environment.TESTING.value):
        db_filename = 'testing.sqlite'

    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), db_filename))
    cursor = conn.cursor()
    return conn, cursor

def migrate():

    load_dotenv()

    """
    Migrate the database.
    """
    Log()('Migrating database...')

    drop_all_tables()

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

def drop_all_tables(silent=False):
    """
    Drop all tables.
    """
    if not silent:
        Log()('Dropping all tables...')

    conn, cursor = connect()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        if table_name[0] != 'sqlite_sequence':
            cursor.execute('''
                DROP TABLE IF EXISTS {}
            '''.format(table_name[0]))
    conn.commit()
    conn.close()
