from __future__ import print_function
import discord, App
from discord.ext import commands
from cogs.file.config import VERSION, NAME

from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.value = [NAME, VERSION]
        self.bot.tree.sync()
        bot.remove_command('help')

        self.helpembed = discord.Embed(title=f"{self.value[0]} v{self.value[1]}", color=0x4441d9)
        self.helpembed.add_field(name="cat", value="gif с котом", inline=False)
        self.helpembed.add_field(name="dog", value="gif с собакой", inline=False)
        self.helpembed.add_field(name="date", value="выводит дату", inline=False)
        self.helpembed.add_field(name="/report", value="жалоба на участника | !report @test", inline=False)
        self.helpembed.add_field(name="smile", value="эмодзи это-го сервера", inline=False)
        self.helpembed.add_field(name="vote", value="голосование (принять,отклонить) *НЕ РАБОТАЕТ*", inline=False)
        self.helpembed.add_field(name="test_command", value="новые команды (самые новые)", inline=False)
        self.helpembed.add_field(name="ctk", value=" | !ctk (message)", inline=False)
        self.helpembed.set_footer(text=self.value[0])
        self.helpembed.set_author(name="by daniil6678#9902")

    @commands.hybrid_command(name="help", with_app_command=True)
    async def help(self, ctx):
        await ctx.send(embed=self.helpembed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
