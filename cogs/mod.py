import asyncio
from logging import getLogger

import discord
from discord.ext import commands

from core import Bot
from . import Plugin

# from discord import app_commands
log = getLogger("Bot")


class Moderation(Plugin):
    def __init__(self, bot: Bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.bot = bot
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync_moder())

    @commands.hybrid_command(name='clear', description='удаляют выбранное кол-во сообщений', with_app_command=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amout: int):
        await ctx.channel.purge(limit=(amout))
        await ctx.send(f'Done({amout})', delete_after=5)

    @commands.hybrid_command(name='kick', description='Кикает пользователя', with_app_command=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason or "No reason given")
        await ctx.send(f"{member.name} был кикнут")

    @commands.hybrid_command(name='ban', description="Не банит пользователя", with_app_command=True)
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(
            f"Бот подумал и пришел к выводу что @{member} слишком хороший для бана и\nпредлогает использовать /kick member:(user) reason:{reason}")


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
