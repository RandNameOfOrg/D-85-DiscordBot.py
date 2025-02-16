import cmd
import os
import sys
import threading
from pathlib import Path
from time import strftime, localtime, sleep

from colorama import Fore, Style
from prettytable import PrettyTable

from core.data import cfg, lang_manager as lm, config, PATH_TO_CONFIG, debug
from core.updater import Updater

__all__ = ("start_print", "RestartRequired", "start_setup", "update", "console")


class RestartRequired(Exception):
    pass


class Console(cmd.Cmd):
    def __init__(self, thread: threading.Thread, prompt="> ", **kwargs):
        super().__init__(**kwargs)
        self.intro = ""
        self.prompt = prompt
        self.thread = thread

    def do_restart(self, arg):
        """Restart the bot"""
        raise RestartRequired

    @staticmethod
    def do_exit(arg):
        """Stop the bot"""
        sys.exit(0)

    @staticmethod
    def do_config(args: list | None = None):
        """Print config"""
        if args and args[0] == "path":
            print(f"PATH_TO_CONFIG: {PATH_TO_CONFIG}")
            return
        print("Config:")
        for k, v in config.items():
            print(f"\t{k}:")
            for kk, vv in v.items():
                if kk == "token" and not args.count("show"):
                    vv = vv[:6] + "..."
                print(f"\t\t{kk}: {vv}")

    def complete_config(self, *args):
        config_args = ["path", "show"]
        return [i for i in config_args if i.startswith(args[0])]

    def do_update(self, args):
        """Update the bot"""
        update()

    def exit(self, line):
        """Exit the program."""
        self.close()

    def get_commands(self):
        return [i.replace("do_", "") for i in self.get_names() if
                i.startswith("do_")]

    def close(self):
        print("\r" + Fore.LIGHTWHITE_EX + Style.BRIGHT + lm["console.exit"] + " [y/N] ", end="")
        ans = input().lower()
        if ans.replace(" ", "").replace("es", "") == "y":
            print("OK")
            raise KeyboardInterrupt

    def precmd(self, line):
        if not self.thread.is_alive():
            print(lm["console.bot_stopped"])
        return line.lower()


def start_print():
    """print a start message"""
    __info = {"name": cfg("Bot", "NAME"), "version": cfg("Settings", "VERSION")}
    tbl = PrettyTable()
    tbl.field_names = [lm["NAME"], f'{__info.get("name")}']
    tbl.add_rows([
        [lm["VERSION"], f'{__info.get("version")}'],
        [lm["START_TIME"], strftime("%H:%M:%S", localtime())],
    ])
    if debug:
        tbl.add_row(["DEBUG", lm["TRUE"]])
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    print(tbl)


def start_setup():
    """print a setup message and fill config.ini"""
    print()
    config["Settings"]["NAME"] = input(
        Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{lm['GET_NAME']}: ")
    config["Settings"]["TOKEN"] = input(
        Fore.LIGHTWHITE_EX + Style.BRIGHT + f"{lm['GET_TOKEN']}: ")
    with open(PATH_TO_CONFIG, "w") as f:
        config.write(f)


def update():
    if sys.argv.count("--noupdate") > 0 or debug:
        return

    def ask_user():
        __update = (input(
            Fore.LIGHTWHITE_EX +
            Style.BRIGHT + f"{lm['ASK_UPDATE']} [Y/n]: ").lower().replace(" ", ""))
        if __update == "y" or __update == "":
            return True
        print(f"{lm['UPDATE_ABORT']}!")
        return False

    __files = []
    for path, _, files in os.walk("cogs"):
        for name in files:
            if name.endswith(".py"):
                __files.append("cogs/" + name)
    __files.append(Path(__file__).absolute())

    updater = Updater(Path(__file__).parent, __files)

    if not updater.getNonUpToDateFiles() and not ask_user() and not updater.need_update:
        return

    updater.updateAll()

    print(Fore.LIGHTWHITE_EX + Style.BRIGHT)
    print(f"{lm['update_success']}! {lm['restart_program']}")


def console(thread: threading.Thread):
    """console function"""
    # NO LOCALIZATION
    if not debug:
        return "wait"
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT, end="")
    sleep(4)
    cl = Console(thread, prompt=f"{Fore.LIGHTWHITE_EX + Style.BRIGHT}{cfg('Bot', 'NAME')}>")

    return cl.cmdloop(intro=lm["console.word"] + " v0.0.2" + "\nAvailable only one language")
