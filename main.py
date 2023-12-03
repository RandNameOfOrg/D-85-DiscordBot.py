"""Start the D-85 bot in discord"""
import asyncio
import logging
import os
import sys
from asyncio import run
from configparser import ConfigParser
from time import strftime, localtime, sleep
from pathlib import Path

from colorama import Fore, Style
from prettytable import PrettyTable
from update__check import check_for_updates, is_up_to_date as iutd

from core import Bot, sqlite
from core.data import PATH_TO_SQLITE, PATH_TO_CONFIG

config = ConfigParser()
config.read(PATH_TO_CONFIG)
cfg = config.get
debug = None
raw_url = "https://raw.githubusercontent.com/RandNameOfOrg/D-85-DiscordBot.py/main"
if cfg("Settings", "DEBUG") == "True" or sys.argv.count("--env") > 0:
    debug = True
else:
    debug = False

if debug:
    import dotenv

    dotenv.load_dotenv()

# if not PATH_TO_SQLITE.exists():
#     sql = sqlite(PATH_TO_SQLITE)
#     sql.create_table()


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


def update():
    def ask_user():
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
        __update = input("Обнаружено обновление! Хотите обновить? [Y/n]: ").lower().replace(" ", "")
        if __update == "y":
            return True
        elif __update == "n":
            print("Обновление отменено!")
            return False
        else:
            return True

    if sys.argv.count("--noupdate") > 0:
        return
    need_update = False
    updated = False
    __files = []
    for path, _, files in os.walk("cogs"):
        for name in files:
            path = Path("cogs/" + name).absolute()
            if name.endswith(".py"):
                __files.append(
                    (path, f"{raw_url}/cogs/{name}"))
    __files.append((Path(__file__).absolute(), "{raw_url}/main.py"))
    for path, url in __files:
        if iutd(path, url):
            need_update = True

    if need_update:
        if not ask_user():
            return

    for path, url in __files:
        if check_for_updates(path, url):
            updated = True
    if updated:
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT)
        print("Обновление успешно завершено! Перезапустите программу")
        exit(code=2)


async def _main():
    """main function"""
    start_print()
    async with Bot() as bot:
        if debug:
            token = os.getenv("TOKEN")
        else:
            token = config['Settings']['TOKEN']
        await bot.start(token, reconnect=True)


if __name__ == "__main__" or sys.argv.count("--start") > 0:
    # exit codes: 0 - error, 1 - success, 2 - update
    update()
    sleep(0.02)
    try:
        run(_main())
    except Exception as e:
        logging.getLogger("MAIN.PY").error(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n\nStopping app ({e.args})")
        exit(code=0)
    except KeyboardInterrupt:
        logging.getLogger("MAIN.PY").warning(Fore.LIGHTRED_EX + Style.BRIGHT + "\n\nStopping app (KeyboardInterrupt)")
        exit(code=1)
    finally:
        print(Style.RESET_ALL, end="")
