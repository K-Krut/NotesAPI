import argparse
from sqlalchemy.orm import Session

from app.crud.notes import update_note_db
from app.database import get_db
from app.models.models import Note


def fix_notes(db: Session, count: int = 40):
    notes = db.query(Note).order_by(Note.id.desc()).all()
    notes_to_fix = notes[:count]
    # notes_to_fix = notes

    for note in notes_to_fix:
        print(update_note_db(db, note, {"is_latest": True}).id)


# python -m app.database.seeds.seed_notes_versions --n 20
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fix db notes")
    parser.add_argument("--n", type=int, default=40, help="notes number")
    args = parser.parse_args()

    db = next(get_db())
    fix_notes(db, args.n)
    db.close()
