import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
from database import get_db_connection

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseScraper:
    """
    A base class for web scrapers, defining the common interface.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_page(self, url):
        """Fetches the content of a single page."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching URL {url}: {e}")
            return None

    def parse_page(self, soup):
        """Parses the page to extract title and content. Must be implemented by subclasses."""
        raise NotImplementedError

    def store_data(self, data):
        """Stores a single data entry into the database."""
        if not data or not data.get('content'):
            logging.warning("Skipping storage due to empty data or content.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO articles (source_url, title, content) VALUES (?, ?, ?)",
                (data['source_url'], data['title'], data['content'])
            )
            conn.commit()
            logging.info(f"Successfully stored data from {data['source_url']}")
        except sqlite3.IntegrityError:
            logging.warning(f"URL already exists in the database: {data['source_url']}")
        except Exception as e:
            logging.error(f"Failed to store data for {data.get('source_url', 'N/A')}: {e}")
        finally:
            conn.close()

    def scrape(self):
        """The main method to orchestrate the scraping process. Must be implemented by subclasses."""
        raise NotImplementedError


class PoeForumsScraper(BaseScraper):
    """
    A scraper specifically for the Path of Exile forums.
    """
    def parse_page(self, soup, url):
        """Parses a forum thread page for the title and the first post's content."""
        title_element = soup.find('h1', class_='layoutBoxTitle')
        title = title_element.get_text(strip=True) if title_element else "No Title Found"

        content_element = soup.select_one('table.forumPostListTable tr:first-child div.content')
        content = content_element.get_text(strip=True) if content_element else None

        if not content:
            logging.warning(f"Could not find content for URL: {url}")
            return None

        return {'source_url': url, 'title': title, 'content': content}

    def find_patch_note_urls(self, news_url="https://www.pathofexile.com/forum/view-forum/patch-notes"):
        """Finds links to individual patch note threads from the main patch notes forum."""
        logging.info(f"Searching for patch note URLs in {news_url}...")
        soup = self.fetch_page(news_url)
        if not soup:
            return []

        # This selector is now corrected based on inspection of the forum HTML
        thread_links = soup.select('td.thread .title a')
        urls = [self.base_url + link['href'] for link in thread_links]

        logging.info(f"Found {len(urls)} potential patch note URLs.")
        return urls

    def scrape(self, max_articles=5):
        """
        Scrapes the latest patch notes from the PoE forums.
        - Finds the latest patch note threads.
        - Parses each thread for its content.
        - Stores the data in the database.
        """
        patch_note_urls = self.find_patch_note_urls()

        if not patch_note_urls:
            logging.error("No patch note URLs found. Aborting scrape.")
            return

        for i, url in enumerate(patch_note_urls):
            if i >= max_articles:
                logging.info(f"Reached max articles limit of {max_articles}.")
                break

            logging.info(f"Scraping URL ({i+1}/{len(patch_note_urls)}): {url}")
            soup = self.fetch_page(url)
            if soup:
                data = self.parse_page(soup, url)
                self.store_data(data)


if __name__ == '__main__':
    # Example of running the enhanced scraper
    poe_scraper = PoeForumsScraper(base_url="https://www.pathofexile.com")
    poe_scraper.scrape(max_articles=5) # Scrape the 5 most recent patch notes
    print("\nScraping process finished. Check logs for details.")