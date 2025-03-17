from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_PASSWORD: str
    # POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    # POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    # POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    # POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    # POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
