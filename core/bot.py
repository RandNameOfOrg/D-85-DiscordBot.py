from typing import Optional
from discord.ext import commands
import discord, configparser, os, time
from colorama import Fore
from .embed import Embed
from logging import getLogger  # , basicConfig
from .data import PATH_TO_CONFIG, MAIN_DIR

log = getLogger("Bot")
# basicConfig(level="INFO")

__all__ = (
    "Bot",
)

config = configparser.ConfigParser()
config.read(PATH_TO_CONFIG)
cfg = config.get


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.default(),
                         aplication_id=cfg('Settings', 'APP_ID'),
                         chank_guild_at_startup=False)

    async def setup_hook(self):
        for f in os.listdir(MAIN_DIR / "cogs"):
            if f.endswith(".py"):
                if not f.startswith("_"):
                    await self.load_extension("cogs." + f[:-3])

    async def on_ready(self) -> None:
        print(Fore.LIGHTWHITE_EX + f"Bot Started as {self.user}")
        log.info(f"Started as {self.user} (ID: {self.user.id}) in " + time.strftime(
            f"%H:%M:%S {Fore.LIGHTWHITE_EX}"))

    async def success(self, content: str, interaction: discord.Interaction, *, ephemeral: Optional[bool] = False,
                      embed: Optional[bool] = True) -> Optional[discord.WebhookMessage]:
        """Send a success message"""
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(embed=Embed(description=content, color=discord.Colour.green()),
                                                       ephemeral=ephemeral)
            return await interaction.response.send_message(
                embed=Embed(description=content, color=discord.Colour.green()), ephemeral=ephemeral)
        else:
            if interaction.response.is_done():
                if interaction.response.is_done():
                    return await interaction.followup.send(content=f"[☑]{content}", ephemeral=ephemeral)
                    return await interaction.response.send_message(content=f"[☑]{content}", ephemeral=ephemeral)

    async def error(self, content: str, interaction: discord.Interaction, *, ephemeral: Optional[bool] = True,
                    embed: Optional[bool] = True) -> Optional[discord.WebhookMessage]:
        """Send a error message"""
        if embed:
            if interaction.response.is_done():
                return await interaction.followup.send(embed=Embed(description=content, color=discord.Colour.red()),
                                                       ephemeral=ephemeral)
            return await interaction.response.send_message(embed=Embed(description=content, color=discord.Colour.red()),
                                                           ephemeral=ephemeral)
        else:
            if interaction.response.is_done():
                if interaction.response.is_done():
                    return await interaction.followup.send(content=f"[❌]{content}", ephemeral=ephemeral)
                    return await interaction.response.send_message(content=f"[❌]{content}", ephemeral=ephemeral)
