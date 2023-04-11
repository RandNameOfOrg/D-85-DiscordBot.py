#!"D:\Program Files\Python\Python311\python.exe"
from colorama import Back, Fore, Style
from core import Bot
import time, asyncio, discord, sqlite3, configparser;config = configparser.ConfigParser()


config.read('config.ini')

def start_print():
    """print a start message"""
    name = config["Settings"]["NAME"]
    print(Fore.LIGHTBLUE_EX + "Начало загрузки бота в " + Fore.GREEN + time.strftime(
        f"%H:%M:%S {Fore.LIGHTWHITE_EX}по локальному времени",
        time.localtime()) + Fore.WHITE + Style.BRIGHT)
    print(Fore.LIGHTYELLOW_EX + '|' + '-' * (
                (23 - len(name)) // 2 - 2) + Fore.GREEN + f'> {name} <' + Fore.LIGHTYELLOW_EX + '-' * (
                  ((23 - len(name)) // 2 - 2) - 1) + '|')
    print('|' + '-' * 21 + '|')
    print(f'|--->version: {config["Settings"]["VERSION"]}<--|')
    print('|---) Bot starting (--|')

async def main():
    """main function"""
    start_print()

    async with Bot() as bot:
        token = config['Settings']['TOKEN']
        await bot.start(token, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())