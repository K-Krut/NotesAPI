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

    return ' '.join(lemmatized_tokens)



def analyze_notes(notes: List[Note]):
    return [preprocess_text(note.details) for note in notes]
