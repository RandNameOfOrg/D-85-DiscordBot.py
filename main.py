"""Start the D-85 bot in discord"""
import logging
import os
import sys
from asyncio import run
from configparser import ConfigParser
from pathlib import Path
from time import strftime, localtime, sleep

from colorama import Fore, Style
from prettytable import PrettyTable

from core import Bot
from core.data import PATH_TO_CONFIG
from core.updater import Updater

config = ConfigParser()
config.read(PATH_TO_CONFIG)
cfg = config.get
debug = None
raw_url = "https://raw.githubusercontent.com/RandNameOfOrg/D-85-DiscordBot.py/main"
if cfg("Settings", "DEBUG") == "True" or sys.argv.count("--debug") > 0:
    debug = True
    print("Debug mode enabled")
else:
    debug = False

if debug or sys.argv.count("--env") > 0:
    import dotenv

    dotenv.load_dotenv()
    config["Settings"]["DEBUG"] = "True"
    config["Settings"]["TOKEN"] = os.getenv("TOKEN")


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
    if sys.argv.count("--noupdate") > 0 or debug:
        return

    def ask_user():
        __update = input(
            Fore.LIGHTWHITE_EX + Style.BRIGHT + "Обнаружено обновление! Хотите обновить? [Y/n]: ").lower().replace(" ",
                                                                                                                   "")
        if __update == "y" or __update == "":
            return True
        print("Обновление отменено!")
        return False

    __files = []
    for path, _, files in os.walk("cogs"):
        for name in files:
            if name.endswith(".py"):
                __files.append("cogs/" + name)
    __files.append(Path(__file__).absolute())

    updater = Updater(Path(__file__).parent, raw_url, __files)

    if not updater.getNonUpToDateFiles():
        return

    if not ask_user():
        return

    updater.updateAll()

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
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + "Запуск бота... TOKEN: " + token[:4] + "***" + Style.RESET_ALL)
        await bot.start(token, reconnect=True)


if __name__ == "__main__" or sys.argv.count("--start-bot") > 0:
    # exit codes: 0 - error, 1 - success, 2 - update
    update()
    sleep(0.02)
    try:
        run(_main())
    except Exception as e:
        logging.getLogger("MAIN.PY").error(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n\nStopping app: {e.args}")
        exit(code=0)
    except KeyboardInterrupt:
        logging.getLogger("MAIN.PY").warning(Fore.LIGHTRED_EX + Style.BRIGHT + "\n\nStopping app (KeyboardInterrupt)")
        exit(code=1)
    finally:
        print(Style.RESET_ALL, end="")
