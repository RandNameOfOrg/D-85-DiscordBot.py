import os.path
from . import Plugin
from core import Bot
from discord.ext import commands
from discord.utils import get
from discord.ui import Button, View
import os, discord, datetime, configparser
#import App #Disabled

__all__ = (
    "Main",
    "setup",
)

class Vote_(discord.ui.View):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    @discord.ui.button(label="Accept", emoji="✅", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{interaction.user} принял {self.title}')

    @discord.ui.button(style=discord.ButtonStyle.red, label="cancel", emoji="❎")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{interaction.user} отказался от {self.title}')

class Main(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.profiles = os.path.abspath(__file__)[:-13] + "cogs\\"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    async def block(self, ctx) -> None:
        await ctx.send('command is blocked')

    @commands.command(description='sync code')
    async def sync_code(self, ctx):
        await self.bot.tree.sync()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)

    @commands.hybrid_command(name='date', description='время по компьютеру на котором запущен бот', with_app_command=True)
    async def date(self, ctx):
        if self.config['Status']['date'] == 'On':
            now = datetime.datetime.now()
            await ctx.send(now.strftime("сейчас %d.%m.%y по local time"))
        else:
            await self.block(ctx)

    @commands.hybrid_command(name='test_command', description='Открый Бета-Тест', with_app_command=True)
    async def test_command(self, ctx: commands.Context):
        await ctx.reply("nothing")

    # @commands.command(description='None') #name='ctk', with_app_command=True ### Off
    # async def ctk(self, ctx, *message):
    #     if self.config['Status']['ctk'] == 'On':
    #         text = ''
    #         for i in message:
    #             text = text + ' ' + i
    #         # await ctx.send_message(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))
    #         await ctx.reply(App.open_dialog(title_="Запрос", text_=f'Что ответить на {text}'))
    #     else:
    #         await self.block(ctx)


    @commands.hybrid_command(name='cat', description='Мем', with_app_command=True)
    async def cat(self, ctx):
        if self.config['Status']['cat'] == 'On':
            await ctx.reply("https://i.gifer.com/JtaW.gif")
        else:
            await self.block(ctx)


    @commands.hybrid_command(name='dog', description='Мем', with_app_command=True)
    async def dog(self, ctx):
        if self.config['Status']['dog'] == 'On':
            await ctx.reply("https://i.gifer.com/2g.gif")
        else:
            await self.block(ctx)

    @commands.hybrid_command(name='smile', description='Эмодзи сервера', with_app_command=True)
    async def smile(self, ctx):
        if self.config['Status']['smile'] == 'On':
            await ctx.send("<:boteon:706935391852167208> ")
        else:
            await self.block(ctx)

    @commands.hybrid_command(name='vote', description='Голосование', with_app_command=True)
    async def vote(self, ctx, *, title):
        if self.config['Status']['dog'] == 'On':
            await ctx.send(embed=discord.Embed(title=title), view=Vote_(title))
        else:
            await self.block(ctx)


async def setup(bot: Bot):
    await bot.add_cog(Main(bot))
