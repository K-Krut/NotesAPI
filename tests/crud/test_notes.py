import pytest

from app.crud.notes import create_note_db, get_note_db
from app.models.models import Note
from app.schemas.notes import NoteSchema

FAKE_NOTE = {
    "id": 1,
    "name": "Almost rich word company water especially certainl",
    "details": "Quickly begin agree prove candidate down nor near. Food chair stock white. Possible hold statement "
               "thought newspaper entire character identify.\nTelevision form large there church customer attention "
               "teach. Let create recent necessary continue ok great.\nPerform during reveal window wide against these."
               "Feeling employee above from ball scene animal. Director organization your join.\nSmile week laugh "
               "myself. Western as letter beautiful popular develop amount.\nAll stop whatever strategy from reduce. "
               "Pull per student national too.\nAlmost energy billion describe they result. Ground respond beat. "
               "Thank shake cold certain second majority.\nLot assume should board. Training class officer minute "
               "artist.\nEffort letter morning would summer position. Teach stand record miss feeling safe standard. "
               "Center thousand capital nothing gas.\nQuite social policy. Make off cover she above movement whose.\n"
               "Involve knowledge company quite sister successful approach. Sit explain everyone simple.\n"
               "Local everyone social finally institution federal skin. Including none yard something try tax major "
               "kitchen.\nSense over common. Style religious modern affect around effort mention. Never officer career "
               "agree seven consumer.\nGeneration list start turn economy let relate. Throughout media receive anyone. "
               "Crime for culture manage.\nRegion program various guess. National develop game. Side fly language.\n"
               "Clear future business popular. Close consumer mother. Quite thought thus four than often.\n"
               "Beyond anything recognize guy.\nRecord necessary skill third someone team. Sometimes hold myself "
               "into you.\nStore fund agency method view wear wall gas. Everybody move recent friend both prevent.\n"
               "Discover body both popular establish front speak. A region federal center foot light human. "
               "Memory choice cost leave say response big sing.\nNational vote pass individual future tree born its. "
               "Each game value positive position environmental minute.\nSeek energy direction price. "
               "Near significant than. Oil few part buy.\nRate card lead law kitchen arrive pretty. "
               "Position cold economy check sit she. During position clearly job.\nState newspaper decide attention "
               "bar phone. Character ball military very.\nThank son tough cost water. While reveal with teacher "
               "company development.\nAttack learn skill performance for ground. Sort inside heavy lot first. "
               "Heart continue miss city.\nHospital available say culture wind. West agreement mouth contain crime "
               "ever network woman. Show hospital event idea region. Near tax player land.\nOffice watch point fire "
               "senior my. Treat member service treat wonder measure network store. Maybe realize set.\nIndeed learn "
               "any view. Media law human other could similar.\nFar my hair each thus recent. Particular discuss us "
               "thousand bag election. Ask tend summer become water.\nDemocratic front difficult because environment "
               "over deep. Add above bill right. Feeling specific entire study support.\nImpact whose sport. Series "
               "happy husband develop pay. Regi",
    "summary": "The text presents a series of fragmented thoughts and ideas related to various topics such as "
               "economics, education, social policies, media, and community interactions. It discusses concepts like "
               "training, individual and collective efforts, the importance of attention in communications, and the "
               "impact of government and local institutions on social dynamics. Additionally, it touches on the "
               "relationship between the economy and various societal elements, such as crime and culture, "
               "and emphasizes the significance of skills, teamwork, and personal development in achieving goals. "
               "Overall, the text reflects a blend of observations and suggestions aimed at improving societal "
               "conditions and fostering engagement in various sectors.",
    "user_id": 1,
    "parent_id": None,
}


@pytest.fixture(scope="module")
def note_sample() -> Note:
    return Note(
        id=FAKE_NOTE["id"],
        name=FAKE_NOTE["name"],
        details=FAKE_NOTE["details"],
        summary=FAKE_NOTE["summary"],
        user_id=FAKE_NOTE["user_id"],
    )


@pytest.fixture(scope="module")
def note_schema_sample() -> NoteSchema:
    return NoteSchema(
        name=FAKE_NOTE["name"],
        details=FAKE_NOTE["details"],
        summary=FAKE_NOTE["summary"],
    )


def test_create_note_db(mock_db, note_schema_sample):
    note = create_note_db(mock_db, note_schema_sample, user_id=FAKE_NOTE["user_id"])

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(note)

    assert isinstance(note, Note)
    assert note.summary == note_schema_sample.summary


def test_get_note_db(mock_db, note_sample):
    mock_db.query().filter().first.return_value = note_sample

    note = get_note_db(mock_db, note_sample.id)

    assert note.name == note_sample.name
    assert note.details == note_sample.details
    assert note.summary == note_sample.summary
    mock_db.query.assert_called_once()
