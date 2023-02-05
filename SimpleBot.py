from __future__ import print_function
import os.path, time

from discord.ext import commands
import os, discord, asyncio
from cogs.file import config
import sqlite3
from colorama import Back, Fore, Style

s = sqlite3.connect('users.db')
s.close()

data = sqlite3.connect('users.db')
cursor = data.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT UNIQUE,
    discord_name TEXT,
    rang INT DEFAULT 0,
    warns INT DEFAULT 0
)""")
data.commit()
data.close()

#logging.basicConfig(level=logging.INFO)
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
    if cursor.fetchall() == []:
        for guild in bot.guilds:
            for member in guild.members:

                cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{member.id}', '{member.name}', 0, 0);")
                data.commit()
    data.close()

@bot.command()
async def sync(ctx) -> None:
    fmt = await bot.tree.sync(guild=ctx.guild)
    await ctx.send(f"synced {len(fmt)}")

prfx = Fore.LIGHTGREEN_EX + Style.BRIGHT
print(Fore.LIGHTBLUE_EX + "Начало загрузки бота в " + Fore.GREEN + time.strftime(f"%H:%M:%S {Fore.LIGHTWHITE_EX}по локальному времени",
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