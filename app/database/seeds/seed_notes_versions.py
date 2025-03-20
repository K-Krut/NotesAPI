import argparse
import random
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Note, User
from faker import Faker
from random import randint

fake = Faker()


def adjust_text(text, updates):
    text_len = len(text)
    updates_len = len(updates)

    if updates_len > text_len:
        updates = updates[:text_len]
        updates_len = len(updates)

    start = randint(0, text_len - updates_len)
    end = start + updates_len
    return text[:start] + updates + text[end:]


def seed_notes_versions(db: Session, count: int = 10):
    notes = db.query(Note).all()
    # notes = db.query(Note).filter(Note.parent_id.isnot(None)).all()
    for _ in range(count):
        parent = random.choice(notes)
        note = Note(
            name=adjust_text(parent.name, fake.sentence(nb_words=randint(1, 10))),
            details=adjust_text(parent.details, fake.text(max_nb_chars=3000)),
            user_id=parent.user_id,
            parent_id=parent.id,
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.add(note)
    db.commit()


# python -m app.database.seeds.seed_notes_versions --n 20
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="seed db with fake notes")
    parser.add_argument("--n", type=int, default=10, help="notes number")
    args = parser.parse_args()

    db = next(get_db())
    seed_notes_versions(db, args.n)
    db.close()
