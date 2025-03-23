import pytest
import random

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

NOTES_DATA = [
    {
        "name": "Случай в Лувре",
        "details": "Знаменитый куратор Жак Соньер метался по залу Ренессанса, пытаясь скрыться от преследователя. "
                   "Он остановился у картины Леонардо и шепнул нечто непонятное, прежде чем рухнуть на мозаичный пол."
    },
    {
        "name": "Код в дневнике",
        "details": "Под вечер она нашла старый дневник деда. Среди исписанных страниц прятался зашифрованный текст. "
                   "Разгадка привела ее к картине в Эрмитаже, где, как оказалось, был спрятан ключ."
    },
    {
        "name": "Тайна подземелий",
        "details": "Экспедиция спустилась в древнее подземелье под собором. Каменные стены дышали холодом, а на полу "
                   "были выцарапаны загадочные символы, похожие на древнееврейские буквы."
    },
    {
        "name": "Исчезновение профессора",
        "details": "Профессор исчез прямо с лекции. Последняя запись на доске — «Veritas» — не давала покоя его студентам. "
                   "Они начали собственное расследование и наткнулись на древнюю карту."
    },
    {
        "name": "Письмо из прошлого",
        "details": "Она получила письмо без маркировки. Внутри — выцветшее фото и фраза: «Смотри на Луну 21-го». "
                   "В ту ночь небо разверзлось, и в небе появился знак."
    },
    {
        "name": "Операция ‘Тетра’",
        "details": "Военные нашли зашифрованный документ во времена холодной войны. Только спустя 40 лет его расшифровали, "
                   "и оказалось, что он содержит пророчество о падении империи."
    },
    {
        "name": "Иероглифы на крыше",
        "details": "На крыше музея были найдены древнеегипетские символы, вырезанные в камне. "
                   "Ни одна камера не зафиксировала, как они появились за одну ночь."
    },
    {
        "name": "Призрак архивов",
        "details": "Ночью в архивах библиотеки начали срабатывать датчики движения. На камерах — только книги, падающие сами по себе. "
                   "Один охранник поклялся, что слышал шепот на латыни."
    },
    {
        "name": "Секретная экспозиция",
        "details": "В подвале музея реставратор случайно обнаружил скрытую комнату с экспонатами, которых не было в каталоге. "
                   "Один из предметов начал издавать странное гудение."
    },
    {
        "name": "Фреска во тьме",
        "details": "При реставрации монастыря была найдена фреска, которую не мог разглядеть ни один рентген. "
                   "Только при свечах проступал силуэт странного существа с крыльями."
    },
    {
        "name": "Записка в гобелене",
        "details": "Во время чистки старинного гобелена из замка Люксембурга, была найдена записка: «Он не умер. Он спит». "
                   "А под ней — координаты заброшенного аббатства."
    },
    {
        "name": "Сигнал из космоса",
        "details": "Астрономы зафиксировали повторяющийся сигнал, который соответствовал последовательности чисел Фибоначчи. "
                   "Сигнал шел с орбиты Сатурна, и никто не смог объяснить его природу."
    },
    {
        "name": "Зеркало времени",
        "details": "Девочка увидела в антикварном зеркале не своё отражение, а комнату прошлого века. "
                   "Когда она моргнула, зеркало треснуло, а на стекле проступили инициалы D.A."
    },
    {
        "name": "Файл под грифом 'X'",
        "details": "Журналистка нашла в сломанном ноутбуке файл без имени. При открытии запускалась заставка: "
                   "«Если ты это читаешь — ты уже в опасности»."
    },
    {
        "name": "Часы обратного отсчета",
        "details": "На остановке установили загадочные часы без стрелок. Но каждую ночь на них загоралось новое число. "
                   "Когда отсчёт дошёл до нуля — электричество исчезло во всём городе."
    }
]


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


@pytest.fixture
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
    return response.json().get("id")


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


def test_create_note_version(client):
    pass


def test_get_note(client):
    pass
    # response = client.get(
    #     "/api/notes/",
    # )


def test_get_note_history(client):
    pass


def test_update_note_fully(client):
    pass


def test_update_note(client):
    pass


def test_delete_note(client):
    pass
