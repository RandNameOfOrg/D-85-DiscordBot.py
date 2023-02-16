from __future__ import print_function

import discord, sqlite3
from discord.ext import commands
from discord import app_commands

voteIdTexts = {}


class slash(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.c_menu = app_commands.ContextMenu(name="test", callback=self.test_)
        self.bot.tree.add_command(self.c_menu)

        self.bot.tree.sync()


    async def test_(self, interaction: discord.Interaction, message: discord.Message):
        await interaction.user.create_dm().send('Wow, you usage new command')
        await interaction.response.send('OK')

    @app_commands.command(name="report", description="пожаловаться на пользователя")
    async def report(self, Interaction: discord.Interaction, member: discord.Member):
        if self.config['Status']['dog'] == 'On':
            data = sqlite3.connect('users.db')
            cursor = data.cursor()
            message = Interaction.response
            db_userWarns = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
            cursor.execute(f"UPDATE users SET warns = {db_userWarns + 1} WHERE id = {member.id}")
            data.commit()
            data.close()
            if db_userWarns + 1 >= 5:
                await message.send_message(embed=discord.Embed(title="❗❗📣ВНИМАНИЕ📣❗❗",
                                                               description=f"У {member.name} уже {db_userWarns + 1} Жалоб!!!",
                                                               colour=discord.Color.red()))
            else:
                await message.send_message('Жалоба отправлена')
        else:
            await Interaction.response.send_message('command is blocked')



    @app_commands.command(name="unreport", description="убирает репорты с пользователя")
    async def unreport(self, Interaction: discord.Interaction, member: discord.Member, number: int = 1):
        data = sqlite3.connect('users.db')
        cursor = data.cursor()
        message = Interaction.response
        cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}")
        db_data = cursor.fetchone()[0]
        cursor.execute(f"SELECT rang FROM users WHERE id = {member.id}")
        if cursor.fetchone()[0] >= 1:
            if db_data > 0 & number == 1:
                cursor.execute(f"UPDATE users SET warns = {db_data - 1} WHERE id = {member.id}")
                data.commit()
            elif db_data >= number:
                cursor.execute(f"UPDATE users SET warns = {db_data - number} WHERE id = {member.id}")
                data.commit()
            else:
                await message.send_message('у данного пользователя нет жалоб')
        else:
            await message.send_message('Слишком низкий уровень')
        data.close()

    # @app_commands.command(name="help", description="Сказать от имени бота")
    # @app_commands.describe(numbers='')
    # @app_commands.choices(numbers=[
    #     discord.app_commands.Choice(name='1 репорт', value=1),
    #     discord.app_commands.Choice(name='2 репорта', value=2),
    #     discord.app_commands.Choice(name='3 репорта', value=3),
    #     discord.app_commands.Choice(name='4 репорта', value=4),
    #     discord.app_commands.Choice(name='5 репортов', value=5),
    # ])


async def setup(bot: commands.Bot):
    await bot.add_cog(slash(bot))
