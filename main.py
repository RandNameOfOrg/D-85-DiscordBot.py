"""Start the D-85 bot in discord"""
from asyncio import run
from colorama import Fore, Style
from core import Bot, sqlite
from core.data import PATH_TO_SQLITE, PATH_TO_CONFIG
from configparser import ConfigParser
from time import strftime, localtime
from prettytable import PrettyTable
from update_check.main import checkForUpdates
import os

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
    tbl = PrettyTable()
    tbl.field_names = ["Имя", f'{cfg("Settings", "NAME")}']
    tbl.add_row(['Версия', f'{cfg("Settings", "VERSION")}'])
    tbl.add_row(["Начало загрузки", strftime("%H:%M:%S", localtime())])
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    print(tbl)


def update_and_run():
    __files = []
    for path, subdirs, files in os.walk("cogs"):
        for name in files:
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
        await bot.start(token, reconnect=True)


if __name__ == "__main__":
    update_and_run()
