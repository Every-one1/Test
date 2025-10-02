import re

def clean_text(raw_text: str) -> str:
    """
    Cleans the raw scraped text by removing boilerplate forum text and other noise.
    """
    # Remove text that is likely part of the forum's UI or boilerplate
    # This is a simple approach; a more robust solution might involve
    # more specific scraping or more advanced NLP to identify the main content.

    # Example patterns to remove (can be expanded)
    boilerplate_patterns = [
        r"Forum Index».*?View Thread",
        r"View Staff Posts",
        r"Post Reply",
        r"Last edited by.*",
        r"Last bumped on.*",
        r"This thread has been automatically archived.*",
        r"Posted by.*?Quote this Post",
        r"Report Forum Post.*",
        r'\"[a-zA-Z0-9#_]+ wrote:.*', # Removes quoted text blocks
    ]

    cleaner_text = raw_text
    for pattern in boilerplate_patterns:
        cleaner_text = re.sub(pattern, "", cleaner_text, flags=re.DOTALL | re.IGNORECASE)

    # Remove excessive newlines and whitespace
    cleaner_text = re.sub(r'\s{2,}', ' ', cleaner_text).strip()

    return cleaner_text

import spacy
from collections import Counter
from string import punctuation

# Load the spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Spacy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

def summarize_text(text: str, num_sentences: int = 3) -> str:
    """
    Generates a simple extractive summary of the text.
    """
    if not nlp:
        return "spaCy model not loaded. Cannot generate summary."

    doc = nlp(text)

    # Filter out stop words and punctuation
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]

    # Calculate word frequencies
    freq_word = Counter(keywords)

    # Normalize frequencies
    max_freq = Counter(keywords).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)

    # Score sentences based on word frequencies
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    # Get the top N sentences
    summarized_sentences = sorted(sent_strength.keys(), key=lambda x: sent_strength[x], reverse=True)[:num_sentences]

    return ' '.join([sent.text for sent in summarized_sentences])

def extract_keywords(text: str, num_keywords: int = 10) -> list:
    """
    Extracts the most common nouns and proper nouns as keywords.
    """
    if not nlp:
        return ["spaCy model not loaded. Cannot extract keywords."]

    doc = nlp(text)

    # Extract nouns and proper nouns, ignoring stop words and punctuation
    keywords = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and token.text not in punctuation]

    # Get the most common keywords
    most_common = Counter(keywords).most_common(num_keywords)

    return [word for word, freq in most_common]

if __name__ == '__main__':
    # This block will now demonstrate all processing functions
    sample_text = """
    Ok hi,I think these numbers are somewhat very weird and I see no use in it as it is clearly worse than the original gem?
    Please correct my math if I am wrong: (ignore AOE for now)== MATH ==Original gem: 1s base duration, 180% on hits and ailments=> Hit DPS:180% per 1s=> Ailment DPS: 180% but difficult to calculate, but you can just keep hitting and wait for aftershocks, you def will not have a timing issue.
    If you scale duration down by 50%, it's 180% per 0.5s, making it 360%.Transfigured gem: 3s base duration, 15% per 0.1s duration for hit, 6% for ailment=> Hit DPS:30*15% = 450% more damage after 3 seconds, so150% per 1sIf you scale this duration to 4seconds: still150% per 1s(600% divided by 4)=> Ailment DPS:30*6% = 180% more damage, after 3 seconds.
    This is also difficult to calculate as bleed duration will probably exceed this duration, so you will need to time it:<bleed duration> - <duration of EQ>== /MATH ==Considering accidentally hitting again within that 3s, your time window is again 3s (you also have this with base gem, but less of an issue because it's only 1s wait).
    """

    cleaned = clean_text(sample_text)
    print("======== CLEANED TEXT ========")
    print(cleaned)

    summary = summarize_text(cleaned)
    print("\n========= SUMMARY ==========")
    print(summary)

    keywords = extract_keywords(cleaned)
    print("\n======== KEYWORDS =========")
    print(keywords)