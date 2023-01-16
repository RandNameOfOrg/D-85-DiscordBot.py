from __future__ import print_function

import discord, json, os, sqlite3
from discord.ext import commands
from discord import app_commands
from cogs.file import config

voteIdTexts = {}


class slash(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        # self.c = self.bot.get_channel(config.report_ch_id)

    @app_commands.command(name="report", description="пожаловаться на пользователя")
    async def report(self, Interaction: discord.Interaction, member: discord.Member):
        data = sqlite3.connect('users.db')
        cursor = data.cursor()
        message = Interaction.response
        cursor.execute(f"SELECT warns FROM users WHERE user_id = {member.id}")
        db_data = cursor.fetchone()[0]
        cursor.execute(f"UPDATE users SET warns = {db_data+1} WHERE user_id = {member.id}")
        data.commit()
        if db_data+1 >= 5:
            await message.send_message(embed=discord.Embed(title="❗❗📣ВНИМАНИЕ📣❗❗",
                                                description=f"У {member.name} уже {db_data+1} Жалоб!!!",
                                                colour=discord.Color.red()))
        else:
            await message.send_message('Жалоба отправлена')
        data.close()


    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await bot.tree.sync(guild=ctx.guild)
        print(f"sn {len(fmt)}")

    # for guild in config.guilds:
    #     asyncio.run(sync(guild=guild))


async def setup(bot: commands.Bot):
    await bot.add_cog(slash(bot), guilds=config.guilds)