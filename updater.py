import requests
from hashlib import sha256
import urllib.request


def is_up_to_date(file_name, url):
    with open(file_name, "r", encoding="utf-8") as f:
        filehash = sha256(f.read().encode('utf-8')).hexdigest()

    urlcode = requests.get(url).text
    urlhash = sha256(urlcode.encode('utf-8')).hexdigest()

    return filehash == urlhash


def update(path, url):
    urllib.request.urlretrieve(url, path)


def check_for_updates(path, url):
    if is_up_to_date(path, url) is False:
        update(path, url)
        return True
    return False
