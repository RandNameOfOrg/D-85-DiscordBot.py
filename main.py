"""Start the D-85 bot in discord"""
import os
import sys
from asyncio import run
from configparser import ConfigParser
from time import strftime, localtime
from pathlib import Path

from colorama import Fore, Style
from prettytable import PrettyTable
from update_check.main import checkForUpdates

from core import Bot, sqlite
from core.data import PATH_TO_SQLITE, PATH_TO_CONFIG

config = ConfigParser()
config.read(PATH_TO_CONFIG)
cfg = config.get
debug = cfg("Settings", "DEBUG")

if debug:
    import dotenv

    dotenv.load_dotenv()

if not PATH_TO_SQLITE.exists():
    sql = sqlite(PATH_TO_SQLITE)
    sql.create_table()


def start_print():
    """print a start message"""
    global cfg
    __info = {"name": cfg("Settings", "NAME"), "version": cfg("Settings", "VERSION")}
    tbl = PrettyTable()
    tbl.field_names = ["Имя", f'{__info.get("name")}']
    tbl.add_row(['Версия', f'{__info.get("version")}'])
    tbl.add_row(["Начало загрузки", strftime("%H:%M:%S", localtime())])
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    print(tbl)


def update_and_run():
    __files = []
    for path, _, files in os.walk("cogs"):
        for name in files:
            path = Path("cogs/" + name).absolute()
            if name.endswith(".py"):
                __files.append(
                    (path, "https://raw.githubusercontent.com/MGS-Daniil/D-85-DiscordBot.py/main/cogs/" + name))
    __files.append((__file__, "https://raw.githubusercontent.com/MGS-Daniil/D-85-DiscordBot.py/main/main.py"))
    for path, url in __files:
        checkForUpdates(path, url)
    run(_main())


async def _main():
    """main function"""
    start_print()

    async with Bot() as bot:
        if debug:
            token = os.getenv("TOKEN")
        else:
            token = config['Settings']['TOKEN']
        if sys.argv[1:] in ["--debug", "-d"]:
            return 1
        await bot.start(token, reconnect=True)


if __name__ == "__main__":
    update_and_run()
