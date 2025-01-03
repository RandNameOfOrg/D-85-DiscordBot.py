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
from core.lc_manager import get_lang_manager
from core.updater import Updater

lang_manager = get_lang_manager()
get_lc_key = lang_manager.get_lc_by_key
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
    config["Bot"]["TOKEN"] = os.getenv("TOKEN")


# if not PATH_TO_SQLITE.exists():
#     sql = sqlite(PATH_TO_SQLITE)
#     sql.create_table()


def start_print():
    """print a start message"""
    global cfg
    __info = {"name": cfg("Bot", "NAME"), "version": cfg("Settings", "VERSION")}
    tbl = PrettyTable()
    tbl.field_names = [get_lc_key("NAME"), f'{__info.get("name")}']
    tbl.add_rows([
        [get_lc_key("VERSION"), f'{__info.get("version")}'],
        [get_lc_key("START_TIME"), strftime("%H:%M:%S", localtime())],
    ])
    if debug:
        tbl.add_row(["DEBUG", get_lc_key("TRUE")])
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    print(tbl)


def start_setup():
    """print a setup message and fill config.ini"""
    global config
    print()
    config["Settings"]["NAME"] = input(
        Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{get_lc_key('GET_NAME')}: ")
    config["Settings"]["TOKEN"] = input(
        Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{get_lc_key('GET_TOKEN')}: ")
    with open(PATH_TO_CONFIG, "w") as f:
        config.write(f)


def update():
    if sys.argv.count("--noupdate") > 0 or debug:
        return

    def ask_user():
        __update = input(
            Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{get_lc_key('ASK_UPDATE')} [Y/n]: ").lower().replace(" ",
                                                                                                                   "")
        if __update == "y" or __update == "":
            return True
        print(f"{get_lc_key('UPDATE_ABORT')}!")
        return False

    __files = []
    for path, _, files in os.walk("cogs"):
        for name in files:
            if name.endswith(".py"):
                __files.append("cogs/" + name)
    __files.append(Path(__file__).absolute())

    updater = Updater(Path(__file__).parent, raw_url, __files)

    if not updater.getNonUpToDateFiles() and not ask_user():
        return

    updater.updateAll()

    print(Fore.LIGHTWHITE_EX + Style.BRIGHT)
    print(f"{get_lc_key('update_success')}! {get_lc_key('restart_program')}")
    exit(code=2)


async def _main():
    """main function"""
    start_print()
    async with Bot() as bot:
        if debug:
            token = os.getenv("TOKEN")
        else:
            token = config['Settings']['TOKEN']
        if not token:
            raise ValueError("No token provided")
            start_setup()
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{get_lc_key('bot_starting')}... TOKEN: " + token[:6] + "***" + Style.RESET_ALL)
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
        logging.getLogger("MAIN.PY").warning(Fore.LIGHTRED_EX + Style.BRIGHT + "\n\nStopping app (User interrupt)")
        exit(code=1)
    finally:
        print(Style.RESET_ALL, end="")
