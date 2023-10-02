import json
import os
from pathlib import Path

from update__check import check_for_updates


class AppData:
    def __init__(self):
        self.data = {}
        self.url = "https://raw.githubusercontent.com/MGS-Daniil/D-85-DiscordBot.py/main"

    def __call__(self, *args, **kwargs):
        return self.data

    def get(self) -> dict:
        self.update()
        with open(Path('.json').absolute(), "r") as f:
            data = json.load(f)
        return data

    def update(self) -> None:
        check_for_updates(Path(".json").absolute(), f"{self.url}/updating_files/.json")
