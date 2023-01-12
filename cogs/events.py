import discord
from discord.ext import commands, tasks

class Com(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.ffile = 'E:\\Программа\\pythonProject1\\cogs\\file'
        self.change_presence.start()


    @tasks.loop(seconds=1.0)
    async def change_presence(self):
        print("Start")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="The Bee Movie"))


    @change_presence.before_loop
    async def before_change_presence(self):
        print("Bot loading")
        await self.bot.wait_until_ready()
        print("Bot loading2")



    @commands.command()
    async def python_skeleton(self, ctx):
        await ctx.channel.purge(limit = 1);
        await ctx.send(f"*Пасхалка обнаружена* \n"
                       f" ░░░░▐▀█▀▌░░░░▀█▄░░░ \n"
                       f"░░░░░▐█▄█▌░░░░░░▀█▄░░ \n"
                       f"░░░░░░▀▄▀░░░▄▄▄▄▄▀▀░░ \n"
                       f"░░░░▄▄▄██▀▀▀▀░░░░░░░ \n"
                       f"░░░█▀▄▄▄█░▀▀░░ \n"
                       f"░░░▌░▄▄▄▐▌▀▀▀░░ Это Скелетик Петя \n"
                       f"▄░▐░░░▄▄░█░▀▀ ░░ Копируйте его и \n"
                       f"▀█▌░░░▄░▀█▀░▀ ░░ вставляйте в каждый\n" 
                       f"░░░░░░░▄▄▐▌▄▄░░░ дискорд сервер\n"
                       f"░░░░░░░▀███▀█░▄░░ Тогда, он сможет\n"
                       f"░░░░░░▐▌▀▄▀▄▀▐▄░░ захватить\n"
                       f"░░░░░░▐▀░░░░░░▐▌░░ весь дискорд\n"
                       f"░░░░░░█░░░░░░░░█░░░░░░░\n"
                       f"░░░░░░█░░░░░░░░█░░░░░░░\n"
                       f"░░░░░░█░░░░")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(
            f"**Добро пожаловать на сервер _Main Test server_** \n"
            f"**Запрещено:**\n\n"
            f"**1.Эпилепсия**\n"
            f"Наказание: Мут\n\n"
            f"**2.18+**\n"
            f"Наказание: Мут\n\n"
            f"**3.Оскорбления**\n"
            f"Наказание: Мут\n\n"
            f"**4.Спам**\n"
            f"Наказание: Фриз\n\n"
            f"**5.Использование каналов не по назначению**\n"
            f"5.Использование каналов не по назначению\n\n"
            f"**6.Взлом учасника или бота**\n"
            f"Наказание: Бан\n\n"
            f"**7.Удаление чужих сообщений, не нарушающие правила**\n"
            f"Наказание: Фриз\n\n"
            f"**8.Упоминание без причины**\n"
            f"Наказание: Мут\n\n"
            f"**9.Отправка вредоносного ПО**\n"
            f"Наказание: Бан")



async def setup(bot: commands.Bot):
    await bot.add_cog(Com(bot))