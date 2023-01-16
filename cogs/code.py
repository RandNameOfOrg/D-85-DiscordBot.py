from __future__ import print_function
import os.path

from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
from discord import app_commands
import os, sys, json, discord, datetime

class code(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.profiles = os.path.abspath(__file__)[:-13] + "cogs\\"

    def set(me):
        with open(profiles + "users.json", "r") as file:
            data = json.load(file)
            file.close()
        with open(profiles + "users.json", "w") as file:
            data[str(me.id)] = {
                "LVL": 0,
                "NAME": me.name,
                "WARNS": 0
            }
            json.dump(data, file, indent=6)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, am: int):
        await ctx.channel.purge(limit=am)

    @commands.command()
    @commands.has_role("admin")
    async def setreports(self, ctx, member: discord.Member):
        set(member)
        await ctx.send("✅ Успешно!")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("команда использована не правильно")
        elif isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingPermissions):
            await ctx.send("")

    @commands.command()
    @commands.has_role('Python Developer')
    async def unreport(self, ctx, mem: discord.Member):
        if ctx.author.id == 849351619878715392:
            await ctx.delete()
            with open(profiles + "users.json", "r") as file:
                data = json.load(file)
                file.close()
            with open(profiles + 'users.json', 'w') as file:
                data[str(mem.id)]['WARNS'] -= 1
                json.dump(data, file, indent=6)
                file.close()
            await ctx.send('Успешно!')
        else:
            await ctx.send("Пользователь не вертифицырован!!")

    @commands.command()
    async def bd(self, ctx, user):
        enter = bd_enter(user)
        await ctx.send(enter)

    def bd_enter(user):
        for i in range(len(users)):
            if user == usersId[i]:
                enter = user + users[i]
            else:
                if user == botsId[i]:
                    enter = user + " обнаружен в базе... это - " + bots[i]
                else:
                    enter = "Ошибка! User не найден. Использование !bd user#0000"
                return enter

    @commands.command()
    async def date(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(now.strftime("сейчас %y.%m.%d по МСК"))

    @commands.command()
    async def test_command(self, ctx):
        await ctx.send("тестовых команд пока нет😟😉 или вы о них не знаете🤐")

    @commands.command()
    async def cat(self, ctx):
        await ctx.send("https://i.gifer.com/JtaW.gif")

    @commands.command(name='dog', help='giv')
    async def dog(self, ctx):
        await ctx.send("https://i.gifer.com/2g.gif")

    @commands.command(help='perimeter')
    async def perimeter(self, ctx, x, y):
        try:
            await ctx.send(int(x) * int(y))
        except:
            await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

    @commands.command(help='3D cube')
    async def cube(self, ctx, x, y, z):
        try:
            await ctx.send(int(x) * int(y) * int(z))
        except:
            await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

    @commands.command(name='difference', help='вычетание')
    async def difference(self, ctx, w, y):
        try:
            await ctx.send(int(w) - int(y))
        except:
            await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

    @commands.command(name='multiply', help='умножение')
    async def multiply(self, ctx, w, y):
        try:
            await ctx.send(int(w) * int(y))
        except:
            await ctx.send(
                embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

    @commands.command(name='divide', help='деление')
    async def divide(self, ctx, w, y):
        if y == "0":
            await ctx.send("wes")
        else:
            await ctx.send(int(w) / int(y))

    @commands.command(name='brush', help='сумма')
    async def brush(self, ctx, w, y):
        await ctx.send(int(w) + int(y))

    @commands.command(name='smile', help='эмодзи это-го сервера')
    async def smile(self, ctx):
        await ctx.send("<:boteon:706935391852167208> ")

    @commands.command(name='kick', help='КИКАЕТ')
    @commands.has_role('admin')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

async def setup(bot: commands.Bot):
    await bot.add_cog(code(bot))