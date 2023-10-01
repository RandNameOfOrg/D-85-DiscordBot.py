"""this is updated update-check package version"""
import requests
from hashlib import sha256
import urllib.request
from tqdm import tqdm


def is_up_to_date(file_name, url):
	with open(file_name, "r", encoding="utf-8") as f:
		file = f.read()
	hash = sha256(file.encode('utf-8')).hexdigest()

	urlcode = requests.get(url).text
	urlhash = sha256(urlcode.encode('utf-8')).hexdigest()

	if hash == urlhash:
		return True
	else:
		return False


def update(path, url):
	for i in tqdm(range(1), desc="Downloading Updates..."):
		urllib.request.urlretrieve(url, path)


def check_for_updates(path, url):
	if is_up_to_date(path, url) is False:
		update(path, url)
		return True
	else:
		return False
