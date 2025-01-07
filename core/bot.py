import configparser
import os
import re
import time
from logging import getLogger  # , basicConfig
from typing import Optional

import discord
from discord.ext import commands

from .data import MAIN_DIR, cfg
from .embed import Embed

log = getLogger("Bot")
# basicConfig(level="INFO")

__all__ = (
    "Bot",
)


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
        print(f"Bot Started as {self.user}")
        log.info(f"Started as {self.user} (ID: {self.user.id}) in " + time.strftime(
            f"%H:%M:%S"))

    async def success(self, content: str, interaction: discord.Interaction, *, ephemeral: Optional[bool] = False,
                      embed: Optional[bool] = True) -> Optional[discord.WebhookMessage]:
        """Send a success message"""
        if interaction.response.is_done():
            if embed:
                return await interaction.followup.send(embed=Embed(description=content, color=discord.Colour.green()),
                                                       ephemeral=ephemeral)
            else:
                return await interaction.followup.send(content=f"[☑]{content}", ephemeral=ephemeral)

    async def error(self, content: str, interaction: discord.Interaction, *, ephemeral: Optional[bool] = True,
                    embed: Optional[bool] = True) -> Optional[discord.WebhookMessage]:
        """Send a error message"""
        if interaction.response.is_done():
            if embed:
                return await interaction.followup.send(embed=Embed(description=content, color=discord.Colour.red()),
                                                       ephemeral=ephemeral)
            else:
                return await interaction.followup.send(content=f"[❌]{content}", ephemeral=ephemeral)
