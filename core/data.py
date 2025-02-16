import configparser
from pathlib import Path

from core.lc_manager import get_lang_manager

__all__ = (
    "PATH_TO_CONFIG",
    "PATH_TO_SQLITE",
    "MAIN_DIR",
    "DATA_DIR",
    "config",
    "cfg",
    "get_lc_key",
    "debug",
)

if __name__ == "__main__":
    raise Exception("This file is not meant to be run directly")

# Paths to files and dirs
MAIN_DIR = Path(__file__).parents[1].absolute()
DATA_DIR = MAIN_DIR / "data"
PATH_TO_SQLITE = DATA_DIR / "users.db"
PATH_TO_CONFIG = MAIN_DIR / "config.ini"

# config
config = configparser.ConfigParser()
config.read(PATH_TO_CONFIG)

cfg = config.get

# localization

lang_manager = get_lang_manager()
get_lc_key = lang_manager.get_lc_by_key

debug = cfg("Settings", "DEBUG")

