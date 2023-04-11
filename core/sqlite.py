import discord
import sqlite3

__all__=(
    "Sqlite",
)

class Sqlite():
    def __init__(self):
        self.pathToSqlite = "../users.db"

        data = sqlite3.connect(self.pathToSqlite)
        cursor = data.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT UNIQUE,
            discord_name TEXT,
            rang INT DEFAULT 0,
            warns INT DEFAULT 0
        )""")
        data.commit()
        data.close()


    def add_users(self, bot):
        with sqlite3.connect(self.pathToSqlite) as data:
            cursor = data.cursor()
            cursor.execute("SELECT * FROM users")
            if cursor.fetchall() == []:
                for guild in bot.guilds:
                    for member in guild.members:
                        cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{member.id}', '{member.name}', 0, 0);")
                        data.commit()