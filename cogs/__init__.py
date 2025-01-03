from __future__ import annotations

import configparser

from discord.ext.commands import Cog
from core import Bot, PATH_TO_CONFIG
from logging import getLogger

log = getLogger(__name__)


class Plugin(Cog):
    def __init__(self, bot: Bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = configparser.ConfigParser()
        self.config.read(PATH_TO_CONFIG)

        self.prefix = self.config['Bot']['msg_prefix']

    async def cog_load(self) -> None:
        log.info(f'Loaded {self.__class__.__name__} cog. ')
