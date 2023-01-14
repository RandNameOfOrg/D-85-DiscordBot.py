from __future__ import print_function
import discord, os.path, pprint, json
from discord.ext import commands
from discord import app_commands

class slash(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @app_commands.command(name="report", description="пожаловаться на пользователя")
    async def report(self, i: discord.Interaction, member: discord.Member):
        with open(profiles + 'users.json', 'r') as file:
            data = json.load(file)
            if data[str(member.id)]['WARNS'] >= 4:
                await i.response.send_message(embed=discord.Embed(title="❗❗📣ВНИМАНИЕ📣❗❗",
                                                   description=f"У {member.name} уже {data[str(member.id)]['WARNS'] + 1} Жалоб!!!",
                                                   colour=discord.Color.red()))
            file.close()


async def setup(bot: commands.Bot):
    await bot.add_cog(slash(bot))