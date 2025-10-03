
from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

# TODO- load secrets from cloud secure vault
class Settings:
    PROJECT_TITLE: str = "Blog app"
    PROJECT_VERSION: str = "0.1.0"

    KEYCLOAK_BASE: str = os.getenv("KEYCLOAK_BASE")
    REALM: str = os.getenv("REALM")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    POSTGRESS_USER: str = os.getenv("POSTGRESS_USER")
    POSTGRESS_PASSWORD: str = os.getenv("POSTGRESS_PASSWORD")
    POSTGRESS_HOST: str = os.getenv("POSTGRESS_HOST")
    POSTGRESS_PORT: str = os.getenv("POSTGRESS_PORT")
    POSTGRESS_DB: str = os.getenv("POSTGRESS_DB")
    DATABASE_URL: str = f"postgresssql://{POSTGRESS_USER}:{POSTGRESS_PASSWORD}@{POSTGRESS_HOST}:{POSTGRESS_PORT}/{POSTGRESS_DB}"





settings = Settings()

