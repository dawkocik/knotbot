import sqlite3
from typing import Union


def create_connection(db_file: Union[bytes, str]) -> None:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()