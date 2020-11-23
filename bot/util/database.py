import sqlite3

from discord.ext.commands import AutoShardedBot

connection: sqlite3.Connection = None
cursor: sqlite3.Cursor = None


class User:
    def __init__(self, discord_id: int, elo: int, voice_time: int, messages_sent: int) -> None:
        self.discord_id = discord_id
        self.elo = elo
        self.voice_time = voice_time
        self.messages_sent = messages_sent


class ServerUser(User):
    def __init__(self, server_id: int, discord_id: int, elo: int, voice_time: int, messages_sent: int) -> None:
        super().__init__(discord_id, elo, voice_time, messages_sent)
        self.server_id = server_id


def database_connect(bot: AutoShardedBot) -> bool:
    try:
        global connection
        connection = sqlite3.connect("ranking.db")
    except sqlite3.Error as e:
        print(e)
        return False
    global cursor
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_id VARCHAR(18),
            elo INTEGER,
            voice_time INTEGER,
            messages_sent INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id VARCHAR(18),
            discord_id VARCHAR(18),
            elo INTEGER,
            messages_sent INTEGER,
            voice_time INTEGER     
        )
    ''')
    return True


def get_global_user(discord_id: int) -> User:
    cursor.execute(
        f'SELECT elo, voice_time, messages_sent FROM users WHERE discord_id = {str(discord_id)}'
    )
    result = cursor.fetchone()
    return User(discord_id, result[0], result[1], result[2])


def get_server_user(server_id: int, discord_id: int) -> ServerUser:
    cursor.execute(f'''
        SELECT elo, voice_time, messages_sent FROM server_users 
        WHERE server_id = {str(server_id)} AND discord_id = {str(discord_id)}
    ''')
    result = cursor.fetchone()
    return ServerUser(server_id, discord_id, result[0], result[1], result[2])
