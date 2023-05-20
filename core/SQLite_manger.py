import sqlite3
import os.path

__all__ = (
    "sqlite",
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


class NotValidError(Exception):
    pass


class Sqlite:
    def __init__(self, sql_path=None):
        if sql_path is None:
            raise NotValidError("You must specify the path to the database file.")
        self.pathToSqlite = sql_path
        if not os.path.exists(self.pathToSqlite):
            with open(self.pathToSqlite, "w") as f:
                f.write("")

    sql_path = ""

    class Field:
        def __init__(self, name=None, type=None, args: list | None = None):
            if name is None or type is None:
                raise NotValidError("You must specify the name and type of the field.")
            self.name = name
            self.type = type
            if args is not None:
                self.args = args

    @connection(sql_path)
    def create_table(self, cursor=None, fields: list | None = None, table_name: str | None = None) -> None:
        if fields is None or table_name is None:
            raise NotValidError("You must specify the table name and its values.")
        cr = f"CREATE TABLE IF NOT EXISTS {table_name}("
        for field in fields:
            cr += f"{field.name} {field.type},"
        cursor.execute(cr)

    @connection(sql_path)
    def re_create(self, cursor=None) -> None:
        cursor.execute("DROP TABLE IF EXISTS users")
        self.create_table()

    @connection(sql_path)
    def load_all_users(self, bot, cursor=None) -> None:
        cursor.execute("SELECT * FROM users")
        if not cursor.fetchall():
            return
        for guild in bot.guilds:
            for member in guild.members:
                cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{member.id}', '{member.name}', 0, 0);")

    @connection(sql_path)
    def add_user(self, user_id, name, cursor=None) -> None:
        cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{user_id}', '{name}', 0, 0);")

    @connection(sql_path)
    def get_user(self, user_id, cursor=None) -> list:
        cursor.execute(f"SELECT * FROM users WHERE userId = '{user_id}'")
        return cursor.fetchone()

    @connection(sql_path)
    def edit_data(self, user_id, data: str, change_to, cursor) -> None:
        cursor.execute(f"UPDATE users SET {data} = {change_to} FROM WHERE userId = '{user_id}'")


def sqlite(sql_path=None):
    sql = Sqlite(sql_path)
    sql.sql_path = sql_path
    return sql
