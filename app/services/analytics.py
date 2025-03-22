import pandas as pd
import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from typing import List
from app.models.models import Note

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


def filter_token(token):
    return token not in stopwords.words('english') and token not in string.punctuation


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if filter_token(token)]

    lemmatized_tokens = [WordNetLemmatizer().lemmatize(token) for token in filtered_tokens]

    return lemmatized_tokens  # return ' '.join(lemmatized_tokens)



def analyze_notes(notes: List[Note]):
    """
    You'll also need to create an Analytics feature with an endpoint that
    analyzes the notes' database.
    This should calculate various statistics including:
      - total word count across all notes,
      - average note length,
      - most common words or phrases,
      - and identify the top 3 longest and shortest notes.
    Use appropriate Python libraries such as NumPy, Pandas, or NLTK for this
    analysis.
    """
    preprocessed_notes = [preprocess_text(note.details) for note in notes]
    all_words = sum([len(words) for words in preprocessed_notes])
    print(len(preprocessed_notes), notes.count())
    average_note_length = int(all_words / len(preprocessed_notes))
    return {"all_words": all_words, "average_note_length": average_note_length}
