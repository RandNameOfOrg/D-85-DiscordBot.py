import discord, configparser
from discord.ext import commands
from discord.ui import View, Select
from core import Bot
from core.data import PATH_TO_CONFIG
from . import Plugin

__all__ = ("Help",)


# region HelpSelect class
class HelpSelect(Select):
    def __init__(self, bot: commands.Bot, name: str):
        super().__init__(placeholder=name, options=[discord.SelectOption(
            label=cog_name, description=cog.__doc__
        ) for cog_name, cog in bot.cogs.items() if cog.__cog_commands__ and cog_name not in ['Com']
        ])
        self.bot = bot

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.bot.get_cog(self.values[0])
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
        await interaction.response.send_message(embed=embed)


# endregion

class Help(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(description='sync help')
    async def sync_help(self, ctx):
        await self.bot.tree.sync()

    @commands.hybrid_command(name="help", description='Все команды бота', with_app_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Help command', description='Help')
        config = configparser.ConfigParser()
        config.read(PATH_TO_CONFIG)
        await ctx.send(embed=embed,
                       view=View().add_item(
                           HelpSelect(self.bot, 'категории бота {}'.format(config.get("Settings", "NAME")))))


async def setup(bot: Bot):
    await bot.add_cog(Help(bot))
