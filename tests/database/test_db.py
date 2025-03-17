from sqlalchemy import text

from app.database import engine


def check_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("successful connection")
    except Exception as e:
        print(e)


check_db_connection()

