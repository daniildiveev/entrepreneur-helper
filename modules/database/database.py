from datetime import datetime
from typing import List, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database_models import User, Request, Base
from modules.setup.config import settings

engine = create_engine(
    settings.database_source
)

Base.metadata.create_all(bind=engine)

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

def add_user_record(times_used_before:int=0) -> None:
    with Session() as session:
        new_user = User(times_used_before=times_used_before)
        session.add(new_user)
        session.commit()

def get_user_requests(user_id:int) -> List[tuple]:
    with Session() as session:
        requests = session.query(Request).filter_by(user_id=user_id).all()

    return requests

def update_user_table(user_id:int) -> None:
    times_used = len(get_user_requests(user_id))

    with Session() as session: 
        session.query(User) \
               .filter_by(user_id=user_id) \
               .update({"times_used_before" : times_used + 1})
        session.commit()