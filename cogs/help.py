from __future__ import print_function
import discord, os.path, apiclient.discovery, httplib2, pprint, json
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.value = "2.1"
        bot.remove_command('help')

        self.helpembed = discord.Embed(title="daniil_85 v" + self.value, color=0x4441d9)
        self.helpembed.set_author(name="помощь")
        self.helpembed.add_field(name="setreports", value="удаление жалоб с участника. !setreports @test",
                                 inline=True)
        self.helpembed.add_field(name="report", value="жалоба на участника !report @test", inline=True)
        self.helpembed.add_field(name="brush", value="сумма n+b", inline=True)
        self.helpembed.add_field(name="cat", value="giv", inline=True)
        self.helpembed.add_field(name="difference", value="вычетание n-b", inline=True)
        self.helpembed.add_field(name="divide", value="деление n/b", inline=True)
        self.helpembed.add_field(name="dog", value=" giv", inline=True)
        self.helpembed.add_field(name="help ", value="Shows this message", inline=True)
        self.helpembed.add_field(name="multiply", value="умножение n*b", inline=True)
        self.helpembed.add_field(name="smile", value="эмодзи это-го сервера", inline=True)
        self.helpembed.add_field(name="perimeter", value="perimeter n*b", inline=True)
        self.helpembed.add_field(name="cube", value="3D cube n * b * c", inline=True)
        self.helpembed.add_field(name="vote", value="голосование (принять,отклонить)", inline=True)
        self.helpembed.add_field(name="date", value="выводит дату", inline=True)
        self.helpembed.add_field(name="setlog",
                                 value="изменяет канал оповещения о включении бота. !Использовать сервер с ботом!", inline=True)
        self.helpembed.add_field(name="предупреждение", value="некоторые команды стоят с задержкой", inline=True)
        self.helpembed.add_field(name="test_command", value="новые команды (но тестовые)", inline=True)
        self.helpembed.set_footer(text="пока всё!")


    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=self.helpembed)

async def setup(bot: commands.Bot):
    cog = bot
    await bot.add_cog(Help(cog))