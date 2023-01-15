from __future__ import print_function

import asyncio

import discord, os.path, pprint, json
from discord.ext import commands
from discord import app_commands
from files import config


class slash(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="report", description="пожаловаться на пользователя")
    async def report(self, interaction: discord.Interaction, member: discord.Member):
        interaction.response.send_massage("test")
        with open(profiles + 'users.json', 'r') as file:
            data = json.load(file)
            if data[str(member.id)]['WARNS'] >= 4:
                await interaction.response.send_message(embed=discord.Embed(title="❗❗📣ВНИМАНИЕ📣❗❗",
                                                   description=f"У {member.name} уже {data[str(member.id)]['WARNS'] + 1} Жалоб!!!",
                                                   colour=discord.Color.red()))
            file.close()


    async def sync(self, guild) -> None:
        fmt = await bot.tree.sync(guild=guild)
        print(f"sn {len(fmt)}")

    for guild in config.guilds:
        asyncio.run(sync(guild=guild))


async def setup(bot: commands.Bot):
    await bot.add_cog(slash(bot), guilds=config.guilds)