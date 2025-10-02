import sys
import os

# Add the 'src' directory to the Python path to allow for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_db_connection
from src.processing import clean_text, summarize_text, extract_keywords

def test_full_processing_on_first_article():
    """
    Fetches the first article and runs the full processing pipeline on it.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT content FROM articles ORDER BY id ASC LIMIT 1")
        row = cursor.fetchone()

        if not row:
            print("No articles found in the database to test.")
            return

        raw_content = row['content']

        print("================ ORIGINAL CONTENT ================")
        print(raw_content)

        cleaned_content = clean_text(raw_content)
        print("\n================ CLEANED CONTENT =================")
        print(cleaned_content)

        summary = summarize_text(cleaned_content)
        print("\n================== SUMMARY =====================")
        print(summary)

        keywords = extract_keywords(cleaned_content)
        print("\n================== KEYWORDS ====================")
        print(keywords)

    finally:
        conn.close()

if __name__ == '__main__':
    test_full_processing_on_first_article()