from pathlib import Path
from typing import List, Literal
import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

env_config = load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = False
    API_V1_STR: str = "/v1"
    BACKEND_PORT: int = 8000

    PROJECT_NAME: str = "Promptify"

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    DB_ENGINE: str = os.getenv("POSTGRES_ENGINE", "postgresql")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")


    DATABASE_URI_FORMAT: str = r"{db_engine}://{user}:{password}@{host}:{port}/{database}"
    DATABASE_URI: str = r"{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    TIME_ZONE: str = 'Europe/Istanbul'

    class Config:
        case_sensitive = True


settings = Settings()
