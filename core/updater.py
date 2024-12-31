import urllib.request
from hashlib import sha256
from pathlib import Path

import requests


class Updater:

    def __init__(self, path: str | Path, url: str, files: list):
        if not Path(path).exists():
            raise ValueError("The path does not exist.")
        self.path = Path(path)
        self.base_url = url
        self.filesToUpdate = [Path(file) for file in files]

    def getNonUpToDateFiles(self):
        return [file for file in self.filesToUpdate if not self.is_up_to_date(file, self.base_url + file.name)]

    def update(self, filename):
        path = self.path / filename

        if not Path(path).exists():
            return False
        urllib.request.urlretrieve(self.path / filename.name, path)
        return True

    def updateAll(self):
        for filename in self.getNonUpToDateFiles():
            self.update(filename)

    def check_for_update(self, filename):
        return self.update(filename) if not self.is_up_to_date(filename,
                                                               self.base_url + filename.name) else False

    def is_up_to_date(self, file_name, url):
        if not Path(self.path / file_name).exists():
            return False
        with open(self.path / file_name, "r", encoding="utf-8") as f:
            filehash = sha256(f.read().encode('utf-8')).hexdigest()

        urlcode = requests.get(url).text.encode('utf-8')
        urlhash = sha256(urlcode).hexdigest()

        return filehash == urlhash
