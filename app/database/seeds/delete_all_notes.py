from sqlalchemy.orm import Session
from app.crud.notes import delete_note_db
from app.database import get_db
from faker import Faker

from app.models.models import Note

fake = Faker()



def seed_notes_versions(db: Session, count: int = 10):
    notes = db.query(Note).all()
    for i in notes:
        delete_note_db(db, int(i.id))
    db.commit()


# python -m app.database.seeds.delete_all_notes --n 20
if __name__ == "__main__":
    db = next(get_db())
    seed_notes_versions(db)
    db.close()
