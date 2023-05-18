import sqlite3
import os.path

__all__ = (
    "Sqlite",
    "connection",
)


def connection(path_to_sqlite_file):
    """ help decorator """

    def f(func):
        def wrapper(*args, **kwargs):
            with sqlite3.connect(path_to_sqlite_file) as data:
                cursor = data.cursor()
                func(*args, **kwargs, cursor=cursor)
                data.commit()

        return wrapper

    return f


class Sqlite:
    def __init__(self, sql_path: str = "../users.db"):
        self.pathToSqlite = sql_path
        if not os.path.exists(self.pathToSqlite):
            with open(self.pathToSqlite, "w") as f:
                f.write("")
        self.create_table()

    @connection("../users.db")
    def create_table(self, cursor=None) -> None:
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            userId INT UNIQUE,
            discord_name TEXT,
            rang INT DEFAULT 0,
            warns INT DEFAULT 0,
            coins INT DEFAULT 0
        )""")

    @connection("../users.db")
    def re_create(self, cursor=None) -> None:
        cursor.execute("DROP TABLE IF EXISTS users")
        self.create_table()

    @connection("../users.db")
    def load_all_users(self, bot, cursor=None) -> None:
        cursor.execute("SELECT * FROM users")
        if not cursor.fetchall():
            return
        for guild in bot.guilds:
            for member in guild.members:
                cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{member.id}', '{member.name}', 0, 0);")

    @connection("../users.db")
    def add_user(self, user_id, name, cursor=None) -> None:
        cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{user_id}', '{name}', 0, 0);")

    @connection("../users.db")
    def get_user(self, user_id, cursor=None) -> list:
        cursor.execute(f"SELECT * FROM users WHERE userId = '{user_id}'")
        return cursor.fetchone()

    @connection("../users.db")
    def edit_data(self, user_id, data: str, change_to, cursor) -> None:
        cursor.execute(f"UPDATE users SET {data} = {change_to} FROM WHERE userId = '{user_id}'")
