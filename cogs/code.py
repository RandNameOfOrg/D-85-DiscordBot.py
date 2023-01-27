from __future__ import print_function
import os.path
from .file import config
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    @commands.command()
    async def date(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(now.strftime("сейчас %y.%m.%d по GMT+3"))

    @commands.hybrid_command(name="test", with_app_command=True, description="Testing")
    async def test_command(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)
        await ctx.reply("скоро все команды станут такими")

    @commands.command()
    async def cat(self, ctx):
        await ctx.reply("https://i.gifer.com/JtaW.gif")

    @commands.command(name='dog', help='giv')
    async def dog(self, ctx):
        await ctx.reply("https://i.gifer.com/2g.gif")

    @commands.command(help='perimeter')
    async def perimeter(self, ctx, x, y):
        await ctx.reply(int(x) * int(y))

    @commands.command(help='3D cube')
    async def cube(self, ctx, x, y, z):
        try:
            await ctx.send(int(x) * int(y) * int(z))
        except:
            await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

    @commands.command(name='smile', help='эмодзи это-го сервера')
    async def smile(self, ctx):
        await ctx.send("<:boteon:706935391852167208> ")

    @commands.command(name='kick', help='КИКАЕТ')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

async def setup(bot: commands.Bot):
    await bot.add_cog(code(bot))