from discord.ext import commands
from colorama import Back, Fore, Style
from core import Sqlite as sql
import os, discord, asyncio, os.path, time, logging, configparser

config = configparser.ConfigParser()
config.read('config.ini')

Sqlite()

#logging.basicConfig(level=logging.INFO) #logging
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, aplication_id=config['Settings']['APP_ID'], shards=2)


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
    print(Fore.LIGHTGREEN_EX + f"Bot Started as {bot.user} (ID: {bot.user.id}) in "+time.strftime(f"%H:%M:%S {Fore.LIGHTWHITE_EX}"))
name = config["Settings"]["NAME"]
data = (23-len(name))//2-2
print(Fore.LIGHTBLUE_EX + "Начало загрузки бота в " + Fore.GREEN + time.strftime(f"%H:%M:%S {Fore.LIGHTWHITE_EX}по локальному времени",
                                                            time.localtime()) + Fore.WHITE + Style.BRIGHT)
print(Fore.LIGHTYELLOW_EX + '|'+'-'*data+Fore.LIGHTGREEN_EX+f'> {name} <'+Fore.LIGHTYELLOW_EX+'-'*(data-1)+'|')
print('|'+'-'*21+'|')
print(f'|--->version: {config["Settings"]["VERSION"]}<--|')
print('|---) Bot starting (--|')


async def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs." + f[:-3])
    token = config['Settings']['TOKEN']
    await bot.start(token)
if __name__ == "__main__":
    asyncio.run(main())