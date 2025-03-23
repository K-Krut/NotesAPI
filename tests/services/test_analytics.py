from app.services.analytics import analyze_notes, prepare_notes_for_response, get_preprocessed_notes, join_all_words, \
    preprocess_text


def test_preprocess_text_removes_stopwords_and_punctuation():
    text = "This is a test sentence, with punctuation and stopwords!"
    tokens = preprocess_text(text)

    assert "test" in tokens
    assert "sentence" in tokens
    assert "a" not in tokens
    assert "," not in tokens


def test_get_preprocessed_notes(fake_analytics_notes):
    preprocessed = get_preprocessed_notes(fake_analytics_notes)

    assert "note" in preprocessed[0]
    assert "text" in preprocessed[0]
    assert "length" in preprocessed[0]


def test_join_all_words(fake_analytics_notes):
    notes_data = get_preprocessed_notes(fake_analytics_notes)
    words = join_all_words(notes_data)

    assert all(isinstance(w, str) for w in words)


def test_prepare_notes_for_response_structure(fake_analytics_notes):
    notes_data = get_preprocessed_notes(fake_analytics_notes)
    prepared = prepare_notes_for_response(notes_data)

    for item in prepared:
        assert "note" in item
        assert "text" not in item


def test_analyze_notes(fake_analytics_notes):
    result = analyze_notes(fake_analytics_notes)

    assert result["all_words"]
    assert result["average_note_length"]
    assert result["most_common_words"]
    assert result["shortest_notes"]
    assert result["longest_notes"]
    assert len(result["shortest_notes"]) <= 3
    assert len(result["longest_notes"]) <= 3
