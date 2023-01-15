from __future__ import print_function
import os.path

from discord.ext import commands, tasks
import os, sys, json, discord, datetime, asyncio
from cogs import help, events
from cogs.files import config

profiles = "cogs\\file\\"
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, aplication_id=config.APP_ID)
voteIdTexts = {}




if not os.path.exists(profiles + 'users.json'):
    with open(profiles + 'users.json', 'w') as file:
        file.write("{}")
        file.close()
    for guild in bot.guilds:
        for member in guild.members:
            set(member)

    def set(me):
        with open(profiles + "users.json", "r") as file:
            data = json.load(file)
            file.close()
        with open(profiles + "users.json", "w") as file:
            data[str(me.id)] = {
                "N1": 0,
                "NAME": me.name,
                "WARNS": 0
            }
            json.dump(data, file, indent=6, )

async def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs." + f[:-3])

w = discord.Game("your massages")

if __name__ == "__main__":
    asyncio.run(main())
    bot.start(config.TOKEN)
    bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, activity=w))