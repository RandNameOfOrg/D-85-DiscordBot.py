import os
import re
import time
from logging import getLogger

import discord
from discord.ext import commands

from .data import MAIN_DIR, cfg

log = getLogger("D-Bot")

__all__ = (
    "Bot",
    "log",
)


def outdated(func):
    async def wrapper(*args, **kwargs):
        log.warning(f"{func.__name__} is dedicated and will be removed soon")
        await func(*args, **kwargs)

    return wrapper


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.default(),
                         aplication_id=cfg('Bot', 'APP_ID'),
                         chank_guild_at_startup=False)

    async def setup_hook(self):
        for f in os.listdir(MAIN_DIR / "cogs"):
            file = re.match(r"^([^_]\w+).py$", f)
            if file is not None:
                await self.load_extension("cogs." + file.group(1))

    async def on_ready(self) -> None:
        print(f"\nBot Started as {self.user}")
        log.info(f"Started as {self.user} (ID: {self.user.id}) in " + time.strftime(
            f"%H:%M:%S"))
