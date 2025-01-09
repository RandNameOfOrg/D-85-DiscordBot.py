import os
import sys
import threading
from pathlib import Path
from time import strftime, localtime, sleep

from colorama import Fore, Style
from prettytable import PrettyTable

from core.data import cfg, get_lc_key, config, PATH_TO_CONFIG, debug, raw_url
from core.updater import Updater

__all__ = ("start_print", "RestartRequired", "start_setup", "update", "console")


class RestartRequired(Exception): pass


def start_print():
    """print a start message"""
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
        __update = (input(
            Fore.LIGHTWHITE_EX +
            Style.BRIGHT + f"{get_lc_key('ASK_UPDATE')} [Y/n]: ").lower().replace(" ", ""))
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

    if not updater.getNonUpToDateFiles() and not ask_user() and not updater.need_update:
        return

    updater.updateAll()

    print(Fore.LIGHTWHITE_EX + Style.BRIGHT)
    print(f"{get_lc_key('update_success')}! {get_lc_key('restart_program')}")


def console(thread: threading.Thread):
    """console function"""
    # NO LOCALIZATION
    if not debug:
        return "wait"
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    sleep(4)
    print(get_lc_key("CONSOLE"), "v0.0.1")
    print("Available only one language")

    while thread.is_alive():
        inp = input(f"{Fore.LIGHTWHITE_EX + Style.BRIGHT}{cfg('Bot', 'NAME')}> ")
        command = inp.lower().split(" ")[0]
        args = inp.lower().replace(command, "").strip().split(" ")

        if command == "exit":
            print("\r" + Fore.LIGHTWHITE_EX + Style.BRIGHT + get_lc_key("CONSOLE_EXIT") + " [y/N] ", end="")
            ans = input().lower()
            if ans.replace(" ", "").replace("es", "") == "y":
                print("OK")
                raise KeyboardInterrupt
        elif command == "config":
            print("Config:")
            for k, v in config.items():
                print(f"\t{k}:")
                for kk, vv in v.items():
                    if kk == "token" and args.count("--show") == 0:
                        vv = vv[:6] + "..."
                    print(f"\t\t{kk}: {vv}")
        elif command == "restart":
            print("Restarting...")
            sleep(0.5)
            exit(code=2)
        else:
            print("Command {} not found".format(command))
