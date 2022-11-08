import os 
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

TOKEN = os.environ.get("TOKEN")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
USER_PASSWORD = os.environ.get("USER_PASSWORD")

NUM_LINKS_TO_GET = 5
QA_MODEL = 'AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru'
SENTENCE_MODEL = 'symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli'
SIMILARITY_THRESHOLD = 0.7

class Settings(BaseModel):
    database_source : str = f'postgresql+psycopg2://{DB_USER}:{USER_PASSWORD}@localhost:5432/{DB_NAME}'

settings = Settings()