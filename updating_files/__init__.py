import json
from pathlib import Path

from core.updater import check_for_updates


class AppData:
    def __init__(self):
        self.data = {}
        self.url = "https://raw.githubusercontent.com/MGS-Daniil/D-85-DiscordBot.py/main"
        self.path = Path('updating_files') / ".json"

    def __call__(self, *args, **kwargs):
        return self.get()

    def get(self) -> dict:
        self.update()
        with open(self.path.absolute(), "r") as f:
            data = json.load(f)
        return data

    def update(self) -> None:
        check_for_updates(self.path.absolute(), f"{self.url}/updating_files/.json")
