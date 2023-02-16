import discord, configparser
from discord.ext import commands
from cogs.file.config import *
from discord.ui import View, Select

class HelpSelect(Select):
    def __init__(self, bot: commands.Bot):
        conig = configparser.ConfigParser()
        conig.read('../config.ini')
        super().__init__(placeholder='категории бота ' + config['Settings']['Name'], options=[discord.SelectOption(
                                label=cog_name, description=cog.__doc__
                            ) for cog_name, cog in bot.cogs.items() if cog.__cog_commands__ and cog_name not in ['Com']
                         ])
        self.bot=bot

    async def callback(self, interaction: discord.Interaction) -> None:
        cog=self.bot.get_cog(self.values[0])
        assert cog

        com_mix=[]
        for i in cog.walk_commands():
            com_mix.append(i)

        for i in cog.walk_app_commands():
            com_mix.append(i)

        embed = discord.Embed(
            title=f'Команда {cog.__cog_name__}',
            description='\n'.join(f"**{command.name}**: `{command.description if command.description !=None else 'None'}`\n" for command in com_mix)
        )
        await interaction.response.send_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.value = [NAME, VERSION]
        bot.remove_command('help')

    @commands.command(description='sync help')
    async def sync_help(self, ctx):
        await self.bot.tree.sync()

    @commands.hybrid_command(name="help", description='Все команды бота', with_app_command=True)
    async def help(self, ctx):
        embed=discord.Embed(title='Help command', description='Help')
        await ctx.send(embed=embed, view=View().add_item(HelpSelect(self.bot)))

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))