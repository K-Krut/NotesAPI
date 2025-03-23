import pytest

NOTE = {
    "name": "summary test",
    "details": "Знаменитый куратор Жак Соньер, пошатываясь, прошел под сводчатой аркой Большой галереи и "
               "устремился к первой попавшейся ему на глаза картине, полотну Караваджо. Ухватился обеими "
               "руками за позолоченную раму и стал тянуть ее на себя, пока шедевр не сорвался со стены и "
               "не рухнул на семидесятилетнего старика Соньера, погребя его под собой.Как и предполагал Соньер, "
               "неподалеку с грохотом опустилась металлическая решетка, преграждающая доступ в этот зал. "
               "Паркетный пол содрогнулся. Где-то вдалеке завыла сирена сигнализации.Несколько секунд куратор "
               "лежал неподвижно, хватая ртом воздух и пытаясь сообразить, на каком свете находится. "
               "Я все еще жив. Потом он выполз из-под полотна и начал судорожно озираться в поисках места, "
}

NOTE_VERSION = {
    "name": "summary test",
    "details": "Знаменитый куратор Жак Соньер, пошатываясь, прошел под сводчатой аркой Большой галереи и "
               "устремился к первой попавшейся ему на глаза картине, полотну Караваджо. Ухватился обеими "
               "руками за позолоченную раму и стал тянуть ее на себя, пока шедевр не сорвался со стены и "
               "не рухнул на семидесятилетнего СТАРИКА Соньера, погребя ЕгО под собой.Как и предполагал Соньер, "
               "неподалеку с грохотом опустилась металлическая решетка, преграждающая доступ в этот зал. "
               "Паркетный пол содрогнулся."
}


@pytest.fixture(scope="module")
def test_user_token(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_notes@gmail.com",
            "password": "pass12345"
        }
    )

    response_data = response.json()
    return response_data.get("access_token")


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


def test_get_notes(client, test_user_token):
    response = client.get(
        "/api/notes/",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )


def test_get_note(client):
    pass
    # response = client.get(
    #     "/api/notes/",
    # )


def test_create_note_version(client):
    pass


def test_get_note_history(client):
    pass


def test_update_note_fully(client):
    pass


def test_update_note(client):
    pass


def test_delete_note(client):
    pass
