import os.path

from .file import config
from discord.ext import commands, tasks
from discord.utils import get
from discord.ui import Button, View
import os, sys, discord, datetime, time
import App



class code(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.profiles = os.path.abspath(__file__)[:-13] + "cogs\\"

    @commands.command()
    async def sync_code(self, ctx):
        await self.bot.tree.sync()
    @commands.hybrid_command(name='clear', with_app_command=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, am: int):
        await ctx.channel.purge(limit=(am+1))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    @commands.hybrid_command(name='date', with_app_command=True)
    async def date(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(now.strftime("сейчас %y.%m.%d по GMT+3"))

    @commands.hybrid_command(name='test_command', with_app_command=True)
    async def test_command(self, ctx: commands.Context):
        await ctx.reply("скоро все команды станут такими")

    @commands.command() #name='ctk', with_app_command=True
    async def ctk(self, ctx, *message):
        text = ''
        for i in message:
            text=text+' '+i
        # await ctx.send_message(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))
        await ctx.reply(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))

    @commands.hybrid_command(name='cat', with_app_command=True)
    async def cat(self, ctx):
        await ctx.reply("https://i.gifer.com/JtaW.gif")

    @commands.hybrid_command(name='dog', with_app_command=True)
    async def dog(self, ctx):
        await ctx.reply("https://i.gifer.com/2g.gif")

    @commands.hybrid_command(name='smile', with_app_command=True)
    async def smile(self, ctx):
        await ctx.send("<:boteon:706935391852167208> ")

    @commands.hybrid_command(name='kick', with_app_command=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    # @commands.command()
    # async def vote(self, ctx, *, title):
    #     try:
    #         msg = await ctx.send(
    #             embed=discord.Embed(title=title),
    #             components=[
    #                 Button(style=ButtonStyle.green, label="Accept", emoji="✅"),
    #                 Button(style=ButtonStyle.red, label="cancellation", emoji="❌")
    #             ]
    #         )
    #         voteIdTexts.update({msg.id: title})
    #     except:
    #         await ctx.send(embed=discord.Embed(description="используйте !vote [text]", colour=discord.Color.red()))


async def setup(bot: commands.Bot):
    await bot.add_cog(code(bot))
