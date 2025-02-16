import json
import re
import urllib.request
from hashlib import sha256
from pathlib import Path

import requests


class Updater:

    def __init__(self, path: str | Path, files: list):
        if not Path(path).exists():
            raise ValueError("The path does not exist.")
        self.path = Path(path)

        if Path(self.path / "updating_files" / ".json").exists():
            with open(self.path / "updating_files" / ".json", "r") as f:
                _ = json.load(f)
                self.branch = _["branch"]
                self.base_url = self.ex_var(_["url"])
        else:
            self.base_url = "https://raw.githubusercontent.com/RandNameOfOrg/D-85-DiscordBot.py/main/"
        self.filesToUpdate = [Path(file) for file in files]
        print(self.branch)
        print(self.base_url)

    def ex_var(self, string):
        """
        :param string:
        :return:
        string with variables
        """
        pattern = re.compile(r'%\{([^}]+)\}')

        with open(self.path / "updating_files" / ".json", "r") as f:
            d = json.load(f)

        return pattern.sub(lambda m: str(d[m.group(1)]), string)

    def getNonUpToDateFiles(self):
        return [file for file in self.filesToUpdate if not self.is_up_to_date(file, self.base_url + file.name)]

    def update(self, filename):
        path = self.path / filename

        if not Path(path).exists():
            return False
        print(f"Updating {filename.name}")
        print(f"From: {self.base_url + filename.name}")
        urllib.request.urlretrieve(path, self.path / filename.name)
        return True

    def updateAll(self):
        for filename in self.getNonUpToDateFiles():
            self.update(filename)

    def check_for_update(self, filename):
        return self.update(filename) if not self.is_up_to_date(filename,
                                                               self.base_url + filename.name) else False

    @property
    def need_update(self):
        if not Path(self.path / "updating_files" / ".json").exists():
            return False

        with open(self.path / "updating_files" / ".json", "r") as f:
            local_data = json.load(f)
        cloud_data = json.load(requests.get(self.base_url + "updating_files/.json").text)
        return local_data["version"] != cloud_data["version"] and local_data["branch"] == cloud_data["branch"]

    def is_up_to_date(self, file_name, url):
        if not Path(self.path / file_name).exists():
            return False
        with open(self.path / file_name, "r", encoding="utf-8") as f:
            filehash = sha256(f.read().encode('utf-8')).hexdigest()

        urlcode = requests.get(url).text.encode('utf-8')
        urlhash = sha256(urlcode).hexdigest()

        return filehash == urlhash
