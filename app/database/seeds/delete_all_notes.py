import argparse
from sqlalchemy.orm import Session
from app.crud.notes import delete_note_db
from app.database import get_db
from faker import Faker

fake = Faker()



def seed_notes_versions(db: Session, count: int = 10):
    for i in range(count):
        delete_note_db(db, i)
    db.commit()


# python -m app.database.seeds.delete_all_notes --n 20
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="seed db with fake notes")
    parser.add_argument("--n", type=int, default=10, help="notes number")
    args = parser.parse_args()

    db = next(get_db())
    seed_notes_versions(db, args.n)
    db.close()
