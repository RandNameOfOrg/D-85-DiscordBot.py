import configparser
from pathlib import Path

__all__ = (
    "PATH_TO_CONFIG",
    "PATH_TO_SQLITE",
    "MAIN_DIR",
    "DATA_DIR",
    "config",
    "cfg",
)

MAIN_DIR = Path(__file__).parents[1].absolute()
DATA_DIR = MAIN_DIR / "data"
PATH_TO_SQLITE = DATA_DIR / "users.db"
PATH_TO_CONFIG = MAIN_DIR / "config.ini"

config = configparser.ConfigParser()
config.read(PATH_TO_CONFIG)

cfg = config.get
