from __future__ import print_function

import asyncio
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands

from core import Bot
from . import Plugin

data = sqlite3.connect('users.db')
cursor = data.cursor()


@app_commands.context_menu(name="пожаловаться на пользователя")
async def report(interaction: discord.Interaction, member: discord.Member):
    db_user_warns = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
    cursor.execute(f"UPDATE users SET warns = {db_user_warns + 1} WHERE id = {member.id}")
    data.commit()
    await interaction.response.send_message('Жалоба отправлена', ephemeral=True)


@app_commands.context_menu(name="Убрать 1 репорт с пользователя")
@commands.has_permissions(manage_channels=True)
async def unreport(interaction: discord.Interaction, member: discord.Member):
    message = interaction.response
    cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}")
    db_data = cursor.fetchone()[0]
    cursor.execute(f"SELECT rang FROM users WHERE id = {member.id}")
    if db_data > 0:
        cursor.execute(f"UPDATE users SET warns = {db_data - 1} WHERE id = {member.id}")
        data.commit()
        await message.send_message('репорт удален')
    else:
        await message.send_message('у данного пользователя нет жалоб')


@app_commands.context_menu(name="Количество жалоб")
async def report_count(interaction: discord.Interaction, member: discord.Member):
    __data = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
    print(__data)
    await interaction.response.send_message(f'Количество жалоб: {__data}', ephermal=True)


class AppCommands(Plugin):
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.bot = bot
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync_2())

    async def sync_2(self):
        await self.bot.tree.sync()


async def setup(bot: Bot):
    __commands = [report, unreport, report_count]
    bot.tree.add_command(report)
    bot.tree.add_command(unreport)
    bot.tree.add_command(report_count)
    await bot.add_cog(AppCommands(bot))
