from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Note
from app.schemas.notes import NoteHistorySchema


# def get_versions(note):
#     return db.query(Note).filter(Note.parent_id == note.id).order_by(Note.id.desc()).all()
#
# def get_recursive_versions(note):
#     versions = get_versions(note)
#

def get_versions_recursive(db: Session, note: Note):
    versions = []

    def fetch_children(note_id):
        children = db.query(Note).filter(Note.parent_id == note_id).order_by(Note.id.desc()).all()
        for child in children:
            versions.append(child)
            fetch_children(child.id)

    fetch_children(note.id)
    return versions


def seed_notes_versions(db: Session):
    notes = db.query(Note).filter(Note.is_latest.isnot(True), Note.parent_id.is_(None)).all()
    for note in notes:
        print(NoteHistorySchema.model_validate(note))
        versions = get_versions_recursive(db, note)

        print('     ', [NoteHistorySchema.model_validate(version) for version in versions])

        print('-' * 15)


# python -m app.database.seeds.seed_notes_versions --n 20
if __name__ == "__main__":

    db = next(get_db())
    seed_notes_versions(db)
    db.close()
