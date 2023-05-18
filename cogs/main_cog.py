import configparser
import datetime
import discord
import os
import os.path

from discord.ext import commands
from core import Bot, Embed
from core.data import PATH_TO_CONFIG
from . import Plugin

# import functools, typing, asyncio
# import App #Disabled

__all__ = (
    "Main",
    "setup",
)


class Vote_(discord.ui.View):
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.rest = 0
        self.resf = 0
        self.golos = []

    @discord.ui.button(label="Accept", emoji="✅", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.golos:
            await interaction.response.send_message(f'вы уже участвовали в голосовании {self.title}', ephemeral=True)
        else:
            self.rest += 1
            self.golos.append(interaction.user)
            await interaction.response.send_message(f'{interaction.user.mention} принял {self.title}')

    @discord.ui.button(style=discord.ButtonStyle.red, label="cancel", emoji="❎")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.golos:
            await interaction.response.send_message(f'вы уже участвовали в голосовании {self.title}', ephemeral=True)
        else:
            self.resf += 1
            self.golos.append(interaction.user)
            await interaction.response.send_message(f'{interaction.user.mention} отказался от {self.title}')


class Main(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.profiles = os.path.abspath(__file__)[:-13] + "cogs\\"
        self.config = configparser.ConfigParser()
        self.config.read(PATH_TO_CONFIG)

    # def to_thread(func: typing.Callable) -> typing.Coroutine:
    #     @functools.wraps(func)
    #     async def wrapper(*args, **kwargs):
    #         return await asyncio.to_thread(func, *args, **kwargs)
    #
    #     return wrapper

    # @to_thread
    # def edit_afer(self, time: int, msgId, *args, **kwargs):
    #     time.sleep(time)
    #     msgId.edit(*args, **kwargs)

    @commands.command(description='sync code')
    async def sync_code(self, ctx):
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    @commands.hybrid_command(name='date', description='время и дата', with_app_command=True)
    async def date(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(now.strftime("сейчас %d.%m.%y %H:%M:%S"))

    @commands.hybrid_command(name='test_command', description='Открытый Бета-Тест', with_app_command=True)
    async def test_command(self, ctx: commands.Context):
        await ctx.reply("nothing")

    # @commands.command(description='None') #name='ctk', with_app_command=True ### Off
    # async def ctk(self, ctx, *message):
    #         text = ''
    #         for i in message:
    #             text = text + ' ' + i
    #         # await ctx.send_message(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))
    #         await ctx.reply(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))

    @commands.hybrid_command(name='cat', description='Мем', with_app_command=True)
    async def cat(self, ctx):
        await ctx.reply("https://i.gifer.com/JtaW.gif")

    @commands.hybrid_command(name='dog', description='Мем', with_app_command=True)
    async def dog(self, ctx):
        await ctx.reply("https://i.gifer.com/2g.gif")

    @commands.hybrid_command(name='smile', description='Эмодзи сервера', with_app_command=True)
    async def smile(self, ctx):
        await ctx.send("<:boteon:706935391852167208> ")

        # @to_thread
        # def vote_helper(self, timeout, message, embed, view):
        #     time.sleep(timeout)
        #     pr = view.resf // (view.resf + view.rest) * 100
        #     embed.description = "отказалось от голосования - {} ({}%),\nприняло голосование - {} ({}%)".format(view.resf,
        #                                                                                                        pr,
        #                                                                                                        view.rest,
        #                                                                                                        100 - pr)
        message.edit(embed=embed, view=view)

    @commands.hybrid_command(name='vote', description='Голосование', with_app_command=True)
    async def vote(self, ctx, *, title):  # , timeout: int = 600):
        view = Vote_(title)
        embed = Embed(title=title)
        embed.set_author(name=ctx.author.name)
        message = await ctx.send(embed=embed, view=view)
        # self.vote_helper(timeout, message, embed, view)


async def setup(bot: Bot):
    await bot.add_cog(Main(bot))
