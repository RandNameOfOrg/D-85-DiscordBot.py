import json
from configparser import ConfigParser

__lc_manager = None


class LocalizationManager:
    def __init__(self):
        from core.data import PATH_TO_CONFIG, DATA_DIR
        self.config = ConfigParser()
        self.config.read(PATH_TO_CONFIG)
        self.LC_DIR = DATA_DIR / 'localization'
        self.__lc_data = {}
        self._lang = self.config.get('Settings', 'lang')
        self.update_data()

    def update_data(self):
        __old_lc_data = self.__lc_data
        self.__lc_data = {}

        for file in self.LC_DIR.iterdir():
            if file.suffix == ".json":
                lc_name = file.name.removesuffix(".json")
                with file.open("r") as f:
                    self.__lc_data[lc_name] = json.loads(f.read())
        # for file in self.LC_DIR.iterdir():
        #     if file.suffix == '.ini':
        #         lc = ConfigParser()
        #         lc.read(file, encoding='utf-8')
        #         lc_dict = {section: dict(lc[section]) for section in lc.sections()}
        #         self.__lc_data[lc_dict['Settings']['lang']] = lc_dict
        if __old_lc_data != self.__lc_data:
            print(f"{self.get_lc_by_key('lc_updated')}!")

    def __call__(self, *args, **kwargs):
        self.update_data()
        return self

    @property
    def lang(self):
        if not self._lang:
            self._lang = 'en'
        return self._lang

    @lang.setter
    def lang(self, lang):
        self.config.set('Settings', 'lang', lang)
        with open(PATH_TO_CONFIG, 'w') as cfg:
            self.config.write(cfg)

    def get_lc_dict(self, lang=None) -> dict:
        """return dict with localization data"""
        lang = lang or self._lang

        translations: dict = self.__lc_data[lang.lower()].copy()
        translations.pop("settings", None)
        # print(f"GET LC DICT: {self.__lc_data[lang.lower()]['translations']}")
        return translations

    def get_lc_by_key(self, key: str, lang: str | None = None, *args, **kwargs):
        """shortcut for self.get_lc_dict[lang][key]"""
        # print(f"GET LC KEY: {key} lang")
        return self.get_lc_dict(lang).get(key.lower(), *args, **kwargs)


def get_lang_manager():
    global __lc_manager
    if not __lc_manager:
        __lc_manager = LocalizationManager()
    return __lc_manager
