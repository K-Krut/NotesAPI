def test_analyze_notes_endpoint(client, bulk_create_notes_analytics, test_analytics_user_token):
    response = client.get(
        "/api/notes/stats",
        headers={"Authorization": f"Bearer {test_analytics_user_token}"}
    )

    assert response.status_code == 200
    response_data = response.json()

    assert response_data.get("all_words")
    assert response_data.get("average_note_length")
    assert response_data.get("most_common_words")
    assert response_data.get("shortest_notes")
    assert response_data.get("longest_notes")
    assert len(response_data["shortest_notes"]) <= 3
    assert len(response_data["longest_notes"]) <= 3
