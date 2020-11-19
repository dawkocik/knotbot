import sqlite3

from bot.knotbot import Knotbot

connection: sqlite3.Connection = None
cursor: sqlite3.Cursor = None


def database_connect(bot: Knotbot) -> bool:
    try:
        global connection
        connection = sqlite3.connect("ranking.db")
    except sqlite3.Error as e:
        print(e)
        return False
    global cursor
    cursor = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_id INTEGER,
        elo INTEGER,
        time_on_voice INTEGER,
        messages_sent INTEGER
        )
        '''
    )
    for guild in bot.guilds:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS server_{0} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ) 
            '''.format(guild.id)  # todo: users
        )
    return True


def get_global_elo(user_id: int) -> int:
    cursor.execute('''
    SELECT global_elo FROM users WHERE discord_id = {0}
    '''.format(user_id))
    return cursor.fetchone()[0]


def get_server_elo(user_id: int, server_id: int) -> int:
    cursor.execute('''
        SELECT global_elo FROM users WHERE discord_id = {0}
        '''.format(user_id))
    return cursor.fetchone()[0]  # todo: yes
