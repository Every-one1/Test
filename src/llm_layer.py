import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.database import get_db_connection
from src.processing import extract_keywords as extract_db_keywords

def configure_gemini():
    """
    Loads the API key from the .env file and configures the Gemini model.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        raise ValueError("GEMINI_API_KEY not found or not set in .env file. Please get a key from https://aistudio.google.com/")

    genai.configure(api_key=api_key)

def find_relevant_articles(query: str, max_articles: int = 3) -> list:
    """
    Finds articles in the database that are relevant to the user's query
    based on keyword matching.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Extract keywords from the user's query
    query_keywords = set(extract_db_keywords(query, num_keywords=5))

    # Fetch all articles to perform a simple keyword search
    cursor.execute("SELECT id, title, content FROM articles")
    all_articles = cursor.fetchall()

    article_scores = {}
    for article in all_articles:
        # Extract keywords from the article's content
        article_keywords = set(extract_db_keywords(article['content'], num_keywords=20))

        # Calculate a simple score based on keyword overlap
        score = len(query_keywords.intersection(article_keywords))

        if score > 0:
            article_scores[article['id']] = score

    # Sort articles by score and get the top N
    sorted_articles = sorted(article_scores.items(), key=lambda item: item[1], reverse=True)
    top_article_ids = [article_id for article_id, score in sorted_articles[:max_articles]]

    if not top_article_ids:
        return []

    # Fetch the full content of the top articles
    placeholders = ','.join('?' for _ in top_article_ids)
    cursor.execute(f"SELECT source_url, title, content FROM articles WHERE id IN ({placeholders})", top_article_ids)

    relevant_articles = cursor.fetchall()
    conn.close()

    return [dict(row) for row in relevant_articles]

def build_prompt(query: str, articles: list) -> str:
    """
    Builds a detailed prompt for the LLM, including the user's query and
    the content of relevant articles as context.
    """
    context = "You are a Path of Exile 2 expert. Your knowledge has been augmented with the following text from recent patch notes and community discussions. Please answer the user's question based on this new information.\n\n"

    for i, article in enumerate(articles, 1):
        context += f"--- Article {i}: {article['title']} ---\n"
        context += f"Source: {article['source_url']}\n\n"
        context += f"{article['content']}\n\n"
        context += f"--- End of Article {i} ---\n\n"

    prompt = f"{context}User Question: {query}\n\nAnswer:"

    return prompt

def ask_gemini(query: str) -> str:
    """
    Orchestrates the process of finding relevant articles, building a prompt,
    and querying the Gemini model.
    """
    try:
        configure_gemini()

        relevant_articles = find_relevant_articles(query)

        if not relevant_articles:
            return "I couldn't find any relevant information in my local database to answer your question. This might be a topic I don't have data on yet."

        prompt = build_prompt(query, relevant_articles)

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        return response.text

    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    # Example of how to use the layer
    test_query = "What are the community's thoughts on the new Earthquake gem?"
    print(f"Testing with query: '{test_query}'")

    # This will fail until the .env file is created and populated
    answer = ask_gemini(test_query)

    print("\n--- Gemini's Response ---")
    print(answer)