from pathlib import Path

__all__ = (
    "PATH_TO_CONFIG",
    "PATH_TO_SQLITE",
    "MAIN_DIR",
)

MAIN_DIR = Path(__file__).parents[1].absolute()
PATH_TO_SQLITE = MAIN_DIR / "users.db"
PATH_TO_CONFIG = MAIN_DIR / "config.ini"
