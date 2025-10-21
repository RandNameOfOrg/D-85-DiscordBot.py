import asyncio

import configparser
import discord
from discord.ext import commands
from discord.ui import View, Select

# from discord import app_commands
from core import Bot
from core.data import PATH_TO_CONFIG
from . import Plugin

__all__ = ("Help",)


class HelpSelect(Select):
    def __init__(self, bot: commands.Bot, name: str):
        super().__init__(placeholder=name, options=[
            discord.SelectOption(
                label=cog_name, description=cog.__doc__
            ) for cog_name, cog in bot.cogs.items() if cog.__cog_commands__ and cog_name not in []
        ])
        self.bot = bot

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.bot.get_cog(self.values[0])
        print("\n\t" + self.values[0])
        assert cog

        com_mix = []
        for i in cog.walk_commands():
            com_mix.append(i)

        for i in cog.walk_app_commands():
            com_mix.append(i)
        embed = discord.Embed(
            title=f'Команды {cog.__cog_name__}',
            description='\n'.join(
                f"**{command.name}**: `{command.description if command.description is not None else 'None'}`\n" for
                command
                in com_mix)
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpView(View):
    def __init__(self, bot: Bot):
        super().__init__()
        cfg = configparser.ConfigParser()
        cfg.read(PATH_TO_CONFIG)
        __bot_name = cfg['Bot']['name']
        self.bot = bot
        self.add_item(HelpSelect(bot, f'команды бота {__bot_name}'))


class Help(Plugin):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        assert isinstance(bot, Bot)
        self.bot = bot
        self.bot.remove_command('help')
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync())

    @commands.hybrid_command(name="help", description='Все команды бота')
    async def help(self, ctx):  # , interaction: discord.Interaction):
        embed = discord.Embed(title='Help command', description='Help')
        # print(interaction.user.name, 'help', embed)
        # await interaction.response.send_message(embed=embed, view=HelpView(self.bot), ephermal=True)
        await ctx.send(embed=embed, view=HelpView(self.bot))

async def setup(bot: Bot):
    await bot.add_cog(Help(bot))
