import argparse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Note

from faker import Faker
from random import randint

fake = Faker()


def seed_main_notes(db: Session, count: int = 10):
    for _ in range(count):
        note = Note(
            name=fake.sentence(nb_words=randint(1, 10)),
            details=fake.text(max_nb_chars=3000),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )
        db.add(note)
    db.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="seed db with fake notes")
    parser.add_argument("--n", type=int, default=10, help="notes number")
    args = parser.parse_args()

    db = next(get_db())
    seed_main_notes(db, args.n)
    db.close()
