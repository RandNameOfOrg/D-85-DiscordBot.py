from typing import Optional
from discord.ext import commands
import discord, configparser, sqlite3
from colorama import Fore
import os
from logging import getLogger; log = getLogger("Bot")

__all__ = (
    "Bot",
)
intents = discord.Intents.all()
intents.members = True
config = configparser.ConfigParser()
config.read('config.ini')


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents,
                         aplication_id=config['Settings']['APP_ID'],
                         chank_guild_at_startup=False)

    async def setup_hook(self):
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                if not f.startswith("_"):
                    await self.load_extension("cogs." + f[:-3]) # + ".plugin")

    async def on_ready(self):
        print(Fore.LIGHTGREEN_EX + f"Bot Started as {self.user} (ID: {self.user.id}) in " + time.strftime(
            f"%H:%M:%S {Fore.LIGHTWHITE_EX}"))

    def success(self, content:str, interaction: discord.Interaction, ephemeral: Optional[bool]):
        """Send a success message"""
        pass

    def error(self, content:str, interaction: discord.Interaction, ephemeral: Optional[bool]):
        """Send a error message"""
        pass

    def sql_connect(self):
        with sqlite3.connect('../users.db') as data:
            cursor = data.cursor()
            cursor.execute("SELECT * FROM users")
            if cursor.fetchall() == []:
                for guild in self.guilds:
                    for member in guild.members:
                        cursor.execute(f"INSERT OR IGNORE INTO users VALUES('{member.id}', '{member.name}', 0, 0);")
                        data.commit()
