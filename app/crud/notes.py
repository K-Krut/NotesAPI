from sqlalchemy.orm import Session

from app.models.models import Note
from app.schemas.notes import NoteSchema


def create_note_db(db: Session, note: NoteSchema, user_id: int) -> Note:
    note_record = Note(**note.model_dump(), user_id=user_id)
    db.add(note_record)
    db.commit()
    db.refresh(note_record)
    return note_record


def get_note_db(db: Session, note_id: int) -> Note | None:
    return db.query(Note).filter(Note.id == note_id).first()


def delete_note_db(db: Session, note_id: int) -> None:
    db.query(Note).filter(Note.id == note_id).delete()
    db.commit()