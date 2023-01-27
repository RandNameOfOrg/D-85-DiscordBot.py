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
        self.helpembed.add_field(name="brush", value="сумма n+b", inline=True)
        self.helpembed.add_field(name="cat", value="giv", inline=True)
        self.helpembed.add_field(name="cube", value="3D cube n * b * c", inline=True)
        self.helpembed.add_field(name="difference", value="вычетание n-b", inline=True)
        self.helpembed.add_field(name="divide", value="деление n/b", inline=True)
        self.helpembed.add_field(name="dog", value=" giv", inline=True)
        self.helpembed.add_field(name="date", value="выводит дату", inline=True)
        self.helpembed.add_field(name="/report", value="жалоба на участника !report @test (отключено)", inline=True)
        self.helpembed.add_field(name="multiply", value="умножение n*b", inline=True)
        self.helpembed.add_field(name="smile", value="эмодзи это-го сервера", inline=True)
        self.helpembed.add_field(name="perimeter", value="perimeter n*b", inline=True)
        self.helpembed.add_field(name="vote", value="голосование (принять,отклонить)", inline=True)
        self.helpembed.add_field(name="предупреждение", value="некоторые команды стоят с задержкой", inline=True)
        self.helpembed.add_field(name="test_command", value="новые команды (но тестовые)", inline=True)
        self.helpembed.add_field(name='*Не в общем доступе*', value='а зачем это писать если заблокиравоно❓', inline=False)
        self.helpembed.add_field(name="command", value="все команды для создателя", inline=True)
        self.helpembed.set_footer(text=self.value[0])
        self.helpembed.set_author(name="daniil6678#9902")

    @app_commands.command(name="help", description="Сказать от имени бота")
    async def slash_help(self, Interaction: discord.Interaction):
        await Interaction.response.send_message(embed=self.helpembed)
    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=discord.Embed(title="Help Command",
                        description="Команда help в новом стиле, и для её исползования пишите /help",
                        colour=discord.Color.orange()))

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))