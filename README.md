# PoE2 LLM Data Augmentation System

This project is a system to gather, process, and present up-to-date information on Path of Exile 2 (PoE2). The primary goal is to supplement the knowledge of an LLM (like Gemini) that has a knowledge cutoff pre-dating significant PoE2 information releases.

## High-Level Architecture

The system is designed with a modular architecture, consisting of the following core components:

1.  **Web Scraper**: An automated component responsible for fetching data from official Path of Exile sources and community wikis.
2.  **Data Processing & Storage**: A layer that cleans the raw scraped data, structures it, and stores it in a local database. It also performs NLP tasks like summarization and keyword extraction.
3.  **LLM Augmentation Layer**: This component takes a user query, retrieves relevant information from the database, and formats it into a prompt for the Gemini LLM.
4.  **User Interface**: A simple interface for users to ask questions and view the LLM's responses.

## Technology Stack

*   **Programming Language**: Python
*   **Web Scraping**: `requests`, `BeautifulSoup4`
*   **Data Storage**: SQLite
*   **NLP**: `spaCy` / `NLTK`
*   **LLM Integration**: `google-generativeai`
*   **Web UI**: Streamlit / Flask