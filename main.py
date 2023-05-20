"""Start the D-85 bot in discord"""
from colorama import Fore, Style
from core import Bot, sqlite
from core.data import PATH_TO_SQLITE, PATH_TO_CONFIG
from time import strftime, localtime
from asyncio import run
from configparser import ConfigParser
from pathlib import Path
from prettytable import PrettyTable

config = ConfigParser()
config.read(PATH_TO_CONFIG)
cfg = config.get

if not PATH_TO_SQLITE.exists():
    sql = sqlite(PATH_TO_SQLITE)
    sql.create_table()


def start_print():
    """print a start message"""
    global cfg
    tbl = PrettyTable()
    tbl.field_names = ["Имя", f'{cfg("Settings", "NAME")}']
    tbl.add_row(['Версия', f'{cfg("Settings", "VERSION")}'])
    tbl.add_row(["Начало загрузки", strftime("%H:%M:%S", localtime())])
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    print(tbl)


async def main():
    """main function"""
    start_print()

    async with Bot() as bot:
        token = config['Settings']['TOKEN']
        await bot.start(token, reconnect=True)


if __name__ == "__main__":
    run(main())
