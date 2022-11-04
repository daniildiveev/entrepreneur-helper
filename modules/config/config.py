import os 
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

TOKEN = os.environ.get("TOKEN")

NUM_LINKS_TO_GET = 5
PATH_TO_JSON = "data_1.json"
USER_DATABASE = 'users.db'
REQUEST_DATABASE = 'requests.db'
QA_MODEL = 'AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru'
SENTENCE_MODEL = 'symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli'
SIMILARITY_THRESHOLD = 0.7

class Settings(BaseModel):
    database_source : str = 'sqlite:///./sql_app.db'

settings = Settings()