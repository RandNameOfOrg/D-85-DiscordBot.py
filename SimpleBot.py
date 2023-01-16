from __future__ import print_function
import os.path
import time

from discord.ext import commands
import os, json, discord, asyncio, logging
from cogs.file import config
import sqlite3
from colorama import Back, Fore, Style

s = sqlite3.connect('users.db')
s.close()

data = sqlite3.connect('users.db')
cursor = data.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INT NOT NULL,
    discord_name TEXT,
    rang INT DEFAULT 0,
    warns INT DEFAULT 0
)""")
data.commit()
data.close()

logging.basicConfig(level=logging.INFO)
profiles = os.path.abspath(__file__)[:-12] + "cogs\\"
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, aplication_id=config.APP_ID, shards=2)
voteIdTexts = {}


@bot.event
async def on_ready():
    data = sqlite3.connect('users.db')
    cursor = data.cursor()
    cursor.execute("SELECT * FROM users")
    if cursor.fetchall() != []:
        for guild in bot.guilds:
            for member in guild.members:
                cursor.execute(f"INSERT INTO users VALUES(?, ?, 0, 0);", (member.id, member.name,))
                data.commit()
    data.close()





prfx = Fore.LIGHTGREEN_EX + Style.BRIGHT
print(Fore.LIGHTBLUE_EX + "Начало загрузки бота в " + Fore.GREEN + time.strftime(f"%H:%M:%S {Fore.LIGHTWHITE_EX}по МСК",
                                                            time.localtime()) + Fore.WHITE + Style.BRIGHT)
print(prfx + '|---> Daniil bot <----|')
print('|---------------------|')
print(f'|--->version: {config.VERSION}<--|')
print('|---) Bot starting (--|')


async def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs." + f[:-3])
    await bot.start(config.TOKEN)
if __name__ == "__main__":
    asyncio.run(main())