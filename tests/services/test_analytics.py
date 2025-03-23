from app.services.analytics import analyze_notes


def test_analyze_notes(fake_analytics_notes):
    result = analyze_notes(fake_analytics_notes)

    assert result["all_words"]
    assert result["average_note_length"]
    assert result["most_common_words"]
    assert result["shortest_notes"]
    assert result["longest_notes"]
    assert len(result["shortest_notes"]) <= 3
    assert len(result["longest_notes"]) <= 3
