import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from typing import List
from app.models.models import Note
from app.schemas.notes import NoteResponseSimple

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


def prepare_notes_for_response(notes_arr: List[dict]) -> List[dict]:
    for record in notes_arr:
        record.pop('text')
        record['note'] = NoteResponseSimple.model_validate(record.get("note"))
    return notes_arr


def analyze_notes(notes: List[Note]):
    """
    You'll also need to create an Analytics feature with an endpoint that
    analyzes the notes' database.
    This should calculate various statistics including:
      - total word count across all notes,
      - average note length,
      - most common words or phrases,
      - and identify the top 3 longest and shortest notes.
    Use appropriate Python libraries such as NumPy, Pandas, or NLTK for this analysis.
    """
    preprocessed_notes = [{"note": note, "text": preprocess_text(note.details)} for note in notes]

    for note in preprocessed_notes:
        note['length'] = len(note.get("text", []))

    preprocessed_notes = sorted(preprocessed_notes, key=lambda note: note.get('length'))
    all_words = sum([note.get("length") for note in preprocessed_notes])
    average_note_length = int(all_words / len(preprocessed_notes))


    return {
        "all_words": all_words,
        "average_note_length": average_note_length,
        "shortest_notes": prepare_notes_for_response(preprocessed_notes[:3]),
        "longest_notes": prepare_notes_for_response(preprocessed_notes[-3:])
    }
