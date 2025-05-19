from __future__ import annotations

from logging import getLogger

from discord.ext.commands import Cog

from core import Bot, config

log = getLogger(__name__)


class Plugin(Cog):
    def __init__(self, bot: Bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = config
        self.prefix = self.config['Bot']['msg_prefix']
        self.cog_load()

    def cog_load(self) -> None:
        log.info(f'Loaded {self.__class__.__name__} cog. ')

    async def sync(self):
        await self.bot.tree.sync()
