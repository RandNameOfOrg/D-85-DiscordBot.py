from __future__ import print_function
import discord, os.path, apiclient.discovery, httplib2, pprint, json
from discord.ext import commands
from discord import app_commands

class slash(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="report")
    async def my_command(self, interaction: discord.Interaction) -> None:
        """ /command-1 """
        await interaction.response.send_message("Hello from command 1!", ephemeral=True)

async def setup(bot: commands.Bot):
    cog = bot
    await bot.add_cog(slash(cog))