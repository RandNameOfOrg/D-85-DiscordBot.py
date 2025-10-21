import configparser
from pathlib import Path

__all__ = (
    "PATH_TO_CONFIG",
    "PATH_TO_DB",
    "MAIN_DIR",
    "DATA_DIR",
    "config",
    "cfg",
    "debug",
)

if __name__ == "__main__":
    raise Exception("This file is not meant to be run directly")

# Paths to files and dirs
MAIN_DIR = Path(__file__).parents[1].absolute()
DATA_DIR = MAIN_DIR / "data"
PATH_TO_DB = DATA_DIR / "users.db"
PATH_TO_CONFIG = MAIN_DIR / "config.ini"

# config
config = configparser.ConfigParser()
config.read(PATH_TO_CONFIG)

cfg = config.get


debug = cfg("Settings", "DEBUG")

