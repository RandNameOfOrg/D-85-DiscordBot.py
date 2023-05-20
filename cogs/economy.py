from . import Plugin
from core import Bot, sqlite
from core.data import PATH_TO_SQLITE
import discord
import asyncio
from discord import app_commands
# from discord.ext import commands
from logging import getLogger

log = getLogger("Bot")


class EconomySys(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.sqlite = sqlite(PATH_TO_SQLITE)
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync_q())

    async def sync_q(self):
        await self.bot.tree.sync()

    @app_commands.command(name="balance", description="Выводит текущий баланс")
    async def show_balance(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Текущий баланс пользователя {interaction.user.mention}: {self.sqlite.get_user(interaction.user.id)}",
            ephemeral=True)


async def setup(bot: Bot):
    await bot.add_cog(EconomySys(bot))
