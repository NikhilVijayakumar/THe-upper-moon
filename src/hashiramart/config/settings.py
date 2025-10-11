# hashiramart/config/settings.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# --- Load .env file ---
load_dotenv(dotenv_path=".env", encoding="utf-8")

# --- Settings class using BaseModel instead of BaseSettings ---
class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MLFLOW_BACKEND_STORE_URI: str = os.getenv("MLFLOW_BACKEND_STORE_URI")
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: str = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD")
    AIRFLOW_USER: str = os.getenv("AIRFLOW_USER")
    AIRFLOW_FIRST: str = os.getenv("AIRFLOW_FIRST")
    AIRFLOW_LAST: str = os.getenv("AIRFLOW_LAST")
    AIRFLOW_EMAIL: str = os.getenv("AIRFLOW_EMAIL")
    AIRFLOW_PASS: str = os.getenv("AIRFLOW_PASS")




# --- Create a single global instance ---
settings = Settings()
