# import mariadb
import sqlite3
import os

# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="db_user",
#         password="db_user_passwd",
#         host="192.0.2.1",
#         port=3306,
#         database="employees"

#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

# # Get Cursor
# cur = conn.cursor()

def connect():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'dev.sqlite'))
    cursor = conn.cursor()
    return conn, cursor

def migrate():
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