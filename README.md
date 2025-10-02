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

## Installation and Setup

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

*   **Python 3.8+**: Ensure you have Python 3.8 or a newer version installed. You can check your version with `python3 --version`.

### 2. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Download the NLP Model

The system uses the `spaCy` library for Natural Language Processing. You need to download the English language model it relies on.

```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

### 5. Set Up Your API Key

The application requires a Google Gemini API key to function.

1.  **Rename the example file**:
    ```bash
    mv .env.example .env
    ```
2.  **Edit the `.env` file**: Open the `.env` file in a text editor and replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key. You can get a key from [Google AI Studio](https://aistudio.google.com/).

### 6. Populate the Database

Before you can ask the LLM questions, you need to populate the local database with up-to-date information from the web.

1.  **Initialize the database** (this creates the `poe_data.db` file and the necessary tables):
    ```bash
    python3 src/database.py
    ```
2.  **Run the scraper** (this will find the latest patch notes, scrape them, and save them to the database):
    ```bash
    python3 src/scraper.py
    ```

### 7. Run the Application

Once the setup is complete, you can launch the Streamlit web interface.

```bash
streamlit run app.py
```

This will start a local web server, and you can access the application in your browser at the provided URL (usually `http://localhost:8501`).