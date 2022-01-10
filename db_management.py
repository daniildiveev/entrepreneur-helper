import sqlite3
import os

def add_record(db_path: str, user_id: int, times_used: int) -> None:
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    try:
        cursor.execute('''CREATE TABLE USERS(
        USER_ID INTEGER PRIMARY KEY,
        USED_BEFORE INTEGER)''')

        print('Successfully created database USERS')
    except:
        print('Successfully found database USERS')

    cursor.execute(f'''INSERT INTO USERS VALUES(
                    {user_id}, {times_used})''')
    connection.commit()
    connection.close()

    print('Record added successfully!')


def get_user_stats(db_path: str, user_id: int):
    if not os.path.exists(db_path): raise FileNotFoundError(f'There is no file {db_path}')

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(f'''SELECT USED_BEFORE
                       FROM USERS
                       WHERE USER_ID = {user_id}''')

    data = cursor.fetchall()

    return data


