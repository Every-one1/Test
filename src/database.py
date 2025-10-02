import sqlite3
import os

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    db_path = 'data/poe_data.db'

    # Create the 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """
    Initializes the database and creates the 'articles' table if it doesn't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL UNIQUE,
            scrape_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()