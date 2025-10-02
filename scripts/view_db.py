import sqlite3

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    db_path = 'data/poe_data.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def view_all_articles():
    """
    Retrieves and prints all articles from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, source_url, title, scrape_date FROM articles")
        rows = cursor.fetchall()

        if not rows:
            print("No articles found in the database.")
            return

        print("Articles currently in the database:")
        for row in rows:
            print(f"  ID: {row['id']}, URL: {row['source_url']}, Title: {row['title']}, Scraped: {row['scrape_date']}")

    except sqlite3.Error as e:
        print(f"An error occurred while querying the database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    view_all_articles()