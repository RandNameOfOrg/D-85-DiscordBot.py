from __future__ import annotations
from colorama import Back, Fore, Style
from core import Bot
import configparser, asyncio, discord, sqlite3, time

config = configparser.ConfigParser()
config.read('config.ini')

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

async def main():
    """main function"""
    name = config["Settings"]["NAME"]
    print(Fore.LIGHTBLUE_EX + "Начало загрузки бота в " + Fore.GREEN + time.strftime(
        f"%H:%M:%S {Fore.LIGHTWHITE_EX}по локальному времени",
        time.localtime()) + Fore.WHITE + Style.BRIGHT)
    print(Fore.LIGHTYELLOW_EX + '|' + '-' * ((23 - len(name)) // 2 - 2) + Fore.LIGHTGREEN_EX + f'> {name} <' + Fore.LIGHTYELLOW_EX + '-' * (
                ((23 - len(name)) // 2 - 2) - 1) + '|')
    print('|' + '-' * 21 + '|')
    print(f'|--->version: {config["Settings"]["VERSION"]}<--|')
    print('|---) Bot starting (--|')


    async with Bot() as bot:
        token = config['Settings']['TOKEN']
        await bot.start(token, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())