from pathlib import Path

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_config = load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True
    API_V1_STR: str = "/v1"
    BACKEND_PORT: int = 8000

    PROJECT_NAME: str = "Chat PDF"

    PROJECT_ROOT: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    DB_ENGINE: str = os.getenv("POSTGRES_ENGINE")
    DB_DRIVER: str = os.getenv("POSTGRES_DRIVER", "psycopg2")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD")
    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URI_FORMAT: str = (
        r"{db_engine}+{db_driver}://{user}:{password}@{host}:{port}/{database}"
    )
    DATABASE_URI: str = (
        DATABASE_URI_FORMAT.format(
            db_engine=DB_ENGINE,
            db_driver=DB_DRIVER,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
    )

    MINIO_URL: str = os.getenv("MINIO_URL")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME")

    ELASTICSEARCH_USERNAME: str = os.getenv("ELASTICSEARCH_USERNAME")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD")
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST")
    ELASTICSEARCH_INDEX_NAME: str = os.getenv("ELASTICSEARCH_INDEX_NAME")
    ELASTICSEARCH_PORT: int = os.getenv("ELASTICSEARCH_PORT")

    TIME_ZONE: str = "Europe/Istanbul"

    FILE_MAX_SIZE_MB: int = 20

    LLM_MODEL: str = "gemini-1.5-flash"

    SYSTEM_PROMPT: str = ("You are a helpful assistant. "
                               "You will be given a content. "
                               "Answer accordingly to the instructions. "
                               "If you don't know the answer, just say that you don't know."
                               "The content will be between <content></content> tag in the message."
                          "Answer in the same language as the question."
                               )


    class Config:
        case_sensitive = True
        env_config = ".env"


settings = Settings()
