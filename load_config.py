from configparser import ConfigParser
import updating_files as uf
from core.data import PATH_TO_CONFIG

data = uf.AppData()
config = ConfigParser()
config.read(PATH_TO_CONFIG)

print(data())

config.set("Settings", "VERSION", data().get("version"))
