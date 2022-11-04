from datetime import datetime
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import settings
from database_models import User, Requests, Base

engine = create_engine(
    settings.database_source,
    connect_args={"check_same_thread": False}
)

Base.metadata.create_all()

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def add_request_record(user_id:int, query:str) -> None:
    raise NotImplementedError

def add_user_record(user_id:int, times_used:int) -> None:
    raise NotImplementedError

def get_user_stats(user_id:int) -> List[str]:
    raise NotImplementedError

def update_users_table(user_id:int) -> None:
    raise NotImplementedError