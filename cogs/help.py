from __future__ import print_function
import discord
from discord.ext import commands
from cogs.file.config import VERSION, NAME

from discord import app_commands


class Help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.value = [NAME, VERSION]
        bot.remove_command('help')

        self.helpembed = discord.Embed(title=f"{self.value[0]} v{self.value[1]}", color=0x4441d9)
        self.helpembed.add_field(name="cat", value="gif с котом", inline=False)
        self.helpembed.add_field(name="dog", value="gif с собакой", inline=False)
        self.helpembed.add_field(name="date", value="выводит дату", inline=False)
        self.helpembed.add_field(name="/report", value="жалоба на участника | !report @test", inline=False)
        self.helpembed.add_field(name="smile", value="эмодзи это-го сервера", inline=False)
        self.helpembed.add_field(name="vote", value="голосование (принять,отклонить) *НЕ РАБОТАЕТ*", inline=False)
        self.helpembed.add_field(name="test_command", value="новые команды (самые новые)", inline=False)
        self.helpembed.add_field(name="ctk", value=" | !tu (message)", inline=False)
        self.helpembed.set_footer(text=self.value[0])
        self.helpembed.set_author(name="by daniil6678#9902")

    @app_commands.command(name="help", description="help")
    async def slash_help(self, Interaction: discord.Interaction):
        await Interaction.response.send_message(embed=self.helpembed)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=self.helpembed)
        # await self.bot.tree.sync(guild=ctx.guild)
        # await ctx.send(embed=discord.Embed(title="Help Command",
        #                                    description="Команда help в новом стиле, и для её исползования пишите /help",
        #                                    colour=discord.Color.orange()))


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
