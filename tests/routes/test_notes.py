import pytest
import random

from tests.data.notes import NOTE, NOTES_DATA, NOTE_FULLY_UPDATE


@pytest.fixture(scope="module")
def bulk_create_notes(client, test_user_token):
    notes = []

    for i in NOTES_DATA:
        response = client.post(
            "/api/notes/",
            json={
                "name": i.get('name'),
                "details": i.get('details'),
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        notes.append(response.json())

    return notes


@pytest.fixture(scope="module")
def note_with_versions(client, test_user_token):
    headers = {"Authorization": f"Bearer {test_user_token}"}

    original = client.post(
        "/api/notes/",
        json=NOTE,
        headers=headers
    ).json()
    parent_id = original["id"]
    versions = [original]

    for _ in range(3):
        data = random.choice(NOTES_DATA)
        version = client.post(
            "/api/notes/",
            json={
                "name": data['name'],
                "details": data["details"],
                "parent_id": parent_id
            },
            headers=headers
        ).json()
        versions.append(version)
        parent_id = version["id"]

    return {
        "original": versions[0],
        "versions": versions[1:],
        "latest": versions[-1]
    }


@pytest.fixture(scope="module")
def note_for_tests(client, test_user_token):
    response = client.post(
        "/api/notes/",
        json=NOTE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    return response.json()


def test_create_note(client, test_user_token):
    response = client.post(
        "/api/notes/",
        json=NOTE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get("name") == NOTE['name']
    assert response_data.get("details") == NOTE['details']
    assert response_data.get("parent") is None


def test_get_notes(client, test_user_token, bulk_create_notes):
    response = client.get(
        "/api/notes/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("notes")
    assert response_data.get("total") >= len(NOTES_DATA)
    assert response_data.get("offset") >= 10


def test_get_note(client, note_for_tests, test_user_token):
    note = note_for_tests
    response = client.get(
        f"/api/notes/{note.get('id')}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("name") == NOTE['name']
    assert response_data.get("details") == NOTE['details']
    assert response_data.get("parent") is None


def test_get_note_not_found(client, test_user_token):
    response = client.get(
        "/api/notes/99999999999",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404


def test_get_note_access_denied(client, note_for_tests, test_second_user_token):
    response = client.get(
        f"/api/notes/{note_for_tests.get('id')}",
        headers={"Authorization": f"Bearer {test_second_user_token}"}
    )
    assert response.status_code == 403


def test_get_note_with_parent(client, note_with_versions, test_user_token):
    note = note_with_versions.get("latest")

    response = client.get(
        f"/api/notes/{note.get('id')}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("name") == note.get('name')
    assert response_data.get("details") == note.get('details')
    assert response_data.get("parent")
    assert response_data.get("parent").get("id") == note.get('parent').get("id")


def test_create_note_version(client, test_user_token, note_for_tests):
    response = client.post(
        "/api/notes/",
        json={
            "name": "VERSION" + NOTE['name'],
            "details": "VERSION\n" + NOTE['details'],
            "parent_id": note_for_tests.get("id")
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data.get("name")
    assert response_data.get("details")
    assert response_data.get("parent")
    assert response_data.get("parent").get("id") == note_for_tests.get("id")


def test_get_note_history(client, test_user_token, note_with_versions):
    note = note_with_versions.get("latest")

    response = client.get(
        f"/api/notes/{note.get('id')}/history",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("note")
    assert response_data.get("note").get("id") == note.get("id")
    assert response_data.get("versions")


def test_get_note_history_not_found(client, test_user_token):
    response = client.get(
        "/api/notes/999999/history",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404


def test_get_note_history_access_denied(client, note_for_tests, test_second_user_token):
    response = client.get(
        f"/api/notes/{note_for_tests.get('id')}/history",
        headers={"Authorization": f"Bearer {test_second_user_token}"}
    )
    assert response.status_code == 403


def test_update_note(client, note_for_tests, test_user_token):
    note = note_for_tests
    new_name = "PATCH " + NOTE['name']
    response = client.patch(
        f"/api/notes/{note.get('id')}",
        json={
            "name": new_name,
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("name") == new_name
    assert response_data.get("details") == NOTE['details']
    assert response_data.get("parent") is None


def test_update_note_not_found(client, test_user_token):
    response = client.patch(
        "/api/notes/999999",
        json={"name": "Updated"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404


def test_update_note_access_denied(client, note_for_tests, test_second_user_token):
    response = client.patch(
        f"/api/notes/{note_for_tests.get('id')}",
        json={"name": "Updated"},
        headers={"Authorization": f"Bearer {test_second_user_token}"}
    )
    assert response.status_code == 403


def test_update_note_fully(client, note_for_tests, test_user_token):
    note = note_for_tests
    response = client.put(
        f"/api/notes/{note.get('id')}",
        json=NOTE_FULLY_UPDATE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get("name") == NOTE_FULLY_UPDATE['name']
    assert response_data.get("details") == NOTE_FULLY_UPDATE['details']
    assert response_data.get("summary") == NOTE_FULLY_UPDATE['summary']


def test_update_note_fully_not_found(client, test_user_token):
    response = client.put(
        "/api/notes/999999",
        json=NOTE_FULLY_UPDATE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404


def test_update_note_fully_access_denied(client, note_for_tests, test_second_user_token):
    response = client.put(
        f"/api/notes/{note_for_tests.get('id')}",
        json=NOTE_FULLY_UPDATE,
        headers={"Authorization": f"Bearer {test_second_user_token}"}
    )
    assert response.status_code == 403


def test_delete_note(client, note_for_tests, test_user_token):
    response = client.delete(
        f"/api/notes/{note_for_tests.get('id')}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 204


def test_delete_note_not_found(client, test_user_token):
    response = client.delete(
        "/api/notes/999999",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404


def test_delete_note_access_denied(client, test_second_user_token, test_user_token):
    note = client.post(
        "/api/notes/",
        json=NOTE,
        headers={"Authorization": f"Bearer {test_user_token}"}
    ).json()

    response = client.delete(
        f"/api/notes/{note.get('id')}",
        headers={"Authorization": f"Bearer {test_second_user_token}"}
    )
    assert response.status_code == 403
