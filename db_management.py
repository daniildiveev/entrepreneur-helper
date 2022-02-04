import sqlite3
import os
from datetime import datetime
import numpy as np

def add_user_record(db_path: str, user_id: int, times_used: int) -> None:
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute('''CREATE TABLE USERS(
        USER_ID INTEGER PRIMARY KEY,
        USED_BEFORE INTEGER)''')

        print('Successfully created table USERS')
    except:
        print('Successfully found table USERS')

    cursor.execute(f'''INSERT INTO USERS VALUES(
                    {user_id}, {times_used})''')
    connection.commit()
    connection.close()

    print('Record added successfully!')


def get_user_stats(db_path: str, user_id:int) -> list:
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute('''CREATE TABLE USERS(
        USER_ID INTEGER PRIMARY KEY,
        USED_BEFORE INTEGER)''')

        print('Successfully created table USERS')
    except:
        print('Successfully found table USERS')

    cursor.execute(f'''SELECT *
                       FROM USERS
                       WHERE USER_ID = {user_id}''')

    data = cursor.fetchall()
    connection.close()

    return data

def add_request_record(db_path:str, user_id:int, query:str) -> None:
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')
    if not os.environ['REQUESTS_ID']: os.environ['REQUESTS_ID'] = '0' 

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute(f'''CREATE TABLE REQUESTS(
                           USER_ID INTEGER,
                           REQUSET_ID INTEGER PRIMARY KEY,
                           TIME DATETIME,
                           QUERY TEXT)''')

        print('Successfully created REQUESTS table!')
    except sqlite3.OperationalError:
        print('Successfully found REQUESTS table!')

    request_id = int(os.environ['REQUESTS_ID']) + 1

    cursor.execute('''INSERT INTO REQUESTS VALUES(?, ?, ?, ?)''', (user_id, request_id, datetime.now(), query))

    connection.commit()
    connection.close()

    print('Record added successfully!')

def update_users_table(db_path:str, user_id:int) -> None:
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')

    user_id, times_used = get_user_stats(db_path, user_id)[0]

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(f'''DELETE FROM USERS WHERE USER_ID = {user_id}''')
    connection.commit()

    cursor.execute(f'''INSERT INTO USERS VALUES({user_id}, {times_used + 1})''')
    connection.commit()

    connection.close()

    print('Successfully updated USERS database!')



