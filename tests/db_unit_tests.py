import sys
sys.path.insert(0, '/home/diveev/projects/entrepreneur_helper/')
import psycopg2
from modules.database import database as db
from modules.setup import config as cfg

def test_add_request_record():
    db.add_request_record(567, 'test query')
    db.add_request_record(98984, 'test query 2')
    db.add_request_record(567, 'test query 3')


    with psycopg2.connect(f"dbname={cfg.DB_NAME} \
        user={cfg.DB_USER} \
        password={cfg.USER_PASSWORD}") as conn:

        with conn.cursor() as curr:
            curr.execute("SELECT * FROM REQUESTS;")

            data = curr.fetchall()

            assert (567, 1) == data[0][:2] and data[0][-1] == 'test query'
            assert (98984, 2) == data[1][:2] and data[1][-1] == 'test query 2'
            assert (567, 3) == data[2][:2] and data[2][-1] == 'test query 3'
def test_add_user_record():
    db.add_user_record()
    db.add_user_record(45)

    with psycopg2.connect(f"dbname={cfg.DB_NAME} \
        user={cfg.DB_USER} \
        password={cfg.USER_PASSWORD}") as conn:

        with conn.cursor() as curr:
            curr.execute("SELECT * FROM USERS;")

            data = curr.fetchall()

            assert data[0] == (1, 0)
            assert data[1] == (2, 45)

def test_get_user_requests():
    requests = db.get_user_requests(567)
    
    assert requests[0].user_id == 567
    assert requests[0].request_id == 1
    assert requests[0].query == 'test query'

    assert requests[1].user_id == 567
    assert requests[1].request_id == 3
    assert requests[1].query == 'test query 3'

def test_update_user_table():
    user_ids = (1, 2)

    for user_id in user_ids:
        db.update_user_table(user_id)
        times_used = len(db.get_user_requests(user_id))

        with psycopg2.connect(f"dbname={cfg.DB_NAME} \
            user={cfg.DB_USER} \
            password={cfg.USER_PASSWORD}") as conn:

            with conn.cursor() as curr:
                curr.execute(f"SELECT * FROM USERS WHERE user_id={user_id};")

                data = curr.fetchall()

                assert data[0] == (user_id, times_used + 1)
        

