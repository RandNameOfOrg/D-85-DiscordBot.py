from . import Plugin
from core import Bot, Sqlite
import discord
from discord import app_commands
# from discord.ext import commands
from logging import getLogger

log = getLogger("Bot")


class EconomySys(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.sqlite = Sqlite()
        super().__init__(bot)

    @app_commands.command(name="balance", description="Выводит текущий баланс")
    async def show_balance(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Текущий баланс пользователя {interaction.user.mention}: {self.sqlite.get_user(interaction.user.id)}",
            ephemeral=True)


async def setup(bot: Bot):
    await bot.add_cog(EconomySys(bot))
