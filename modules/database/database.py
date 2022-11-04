from datetime import datetime
from typing import List
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from ..config.config import settings
from .database_models import User, Request, Base

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
    with Session() as session:
        values = {
            "user_id" : user_id,
            "time" : datetime.now(), 
            "query" : query
        }

        new_request = Request(**values)
        session.add(new_request)
        session.commit()

def add_user_record(user_id:int, times_used_before:int) -> None:
    with Session() as session:
        new_user = User(user_id=user_id, times_used_before=times_used_before)
        session.add(new_user)
        session.commit()

def get_user_stats(user_id:int) -> List[str]:
    with Session() as session:
        requests = session.query(Request).filter_by(user_id=user_id).all()

    return requests


def update_user_table(user_id:int) -> None:
    user_id, times_used = get_user_stats(user_id)

    with Session() as session: 
        session.query(User) \
               .filter_by(user_id=user_id) \
               .update({"times_used_before" : times_used + 1})
        session.commit()