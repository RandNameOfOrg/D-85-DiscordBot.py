"""Start the D-85 bot in discord"""
import asyncio
import logging
import os
import sys
import threading
from time import sleep

from colorama import Fore, Style

from core import Bot
from core.data import cfg, config, get_lc_key as lc, debug
from runner import *

if cfg("Settings", "DEBUG") == "True" or sys.argv.count("--debug") > 0:
    debug = True
else:
    debug = False

if debug or sys.argv.count("--env") > 0:
    import dotenv

    dotenv.load_dotenv()
    config["Settings"]["DEBUG"] = "True"
    debug = True
    config["Bot"]["TOKEN"] = os.getenv("TOKEN") or config["Bot"]["TOKEN"]
    config["Bot"]["APP_ID"] = os.getenv("APP_ID") or config["Bot"]["APP_ID"]
    print("Debug mode enabled")


# if not PATH_TO_SQLITE.exists():
#     sql = sqlite(PATH_TO_SQLITE)
#     sql.create_table()

async def _main():
    """main function"""
    start_print()
    async with Bot() as bot:
        if debug:
            token = os.getenv("TOKEN")
        else:
            token = config['Settings']['TOKEN']
        if not token:
            raise ValueError(lc["NO_TOKEN"])
            #  start_setup()
        print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
        print(f"{lc('bot_starting')}... TOKEN: " + token[:6] + "***" + Style.RESET_ALL)
        await bot.start(token, reconnect=True)


def run_main_thread():
    """Run the main thread"""
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(_main())


if __name__ == "__main__" or sys.argv.count("--start-bot") > 0:
    # exit codes: 0 - success, 1 - error, 2 - update
    os.system("cls" if os.name == "nt" else "clear")
    os.system(f"title {cfg('Bot', 'NAME')} v{cfg('Settings', 'VERSION')}")
    os.system("chcp 65001")
    code = 0
    try:
        update()
        sleep(0.02)

        bot_task = threading.Thread(target=run_main_thread, name="BOT", daemon=True)
        bot_task.start()
        sleep(0.02)
        if console(bot_task) == "wait":
            bot_task.join()
    except KeyboardInterrupt:
        logging.getLogger("MAIN.PY").warning(Fore.LIGHTRED_EX + Style.BRIGHT + "\n\nStopping app (User interrupt)")
    except RestartRequired:
        logging.getLogger("MAIN.PY").warning(Fore.LIGHTRED_EX + Style.BRIGHT + "\n\nRestarting app")
        code=2
    except Exception as e:
        logging.getLogger("MAIN.PY").error(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n\nStopping app: {e.args}")
        code=1
    finally:
        print(Style.RESET_ALL, end="")
        exit(code=code)
