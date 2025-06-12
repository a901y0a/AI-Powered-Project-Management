import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
API_VERSION = os.getenv("AZURE_API_VERSION")
ALGORITHM = "HS256"

def get_pg_connection():
    return DATABASE_URL