from collections import Counter
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


CUSTOM_FILTER_SYMBOL = "—–…•«»“”"


def filter_token(token: str) -> bool:
    return (token not in stopwords.words('english')
            and token not in string.punctuation and token not in CUSTOM_FILTER_SYMBOL)


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if filter_token(token)]

    return [WordNetLemmatizer().lemmatize(token) for token in filtered_tokens]


def prepare_notes_for_response(notes_arr: List[dict]) -> List[dict]:
    for record in notes_arr:
        record.pop('text')
        record['note'] = NoteResponseSimple.model_validate(record.get("note"))
    return notes_arr


def join_all_words(notes_arr: List[dict]):
    result = []
    for record in notes_arr:
        result.extend(record.get('text'))

    return [word for record in notes_arr for word in record.get("text")]


def get_preprocessed_notes(notes: List[Note]) -> List[dict]:
    result = []
    for note in notes:
        text = preprocess_text(note.details)
        result.append({
            "note": note,
            "text": text,
            "length": len(text)
        })
    return sorted(result, key=lambda x: x.get('length'))


def analyze_notes(notes: List[Note]) -> dict:
    preprocessed_notes = get_preprocessed_notes(notes)
    all_words = join_all_words(preprocessed_notes)
    all_words_num = len(all_words)

    return {
        "all_words": all_words_num,
        "average_note_length": int(all_words_num / len(preprocessed_notes)),
        "most_common_words": Counter(all_words).most_common(20),
        "shortest_notes": prepare_notes_for_response(preprocessed_notes[:3]),
        "longest_notes": prepare_notes_for_response(preprocessed_notes[-3:])
    }
