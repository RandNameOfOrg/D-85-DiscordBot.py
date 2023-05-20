from . import Plugin
from core import Bot
import discord
from discord.ext import commands
from logging import getLogger
import asyncio

# from discord import app_commands
log = getLogger("Bot")


class Moderation(Plugin):
    def __init__(self, bot: Bot):
        self.bot = bot
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync_moder())

    @commands.hybrid_command(name='clear', description='удаляют выбранное кол-во сообщений', with_app_command=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amout: int):
        await ctx.channel.purge(limit=(amout))
        await ctx.send(f'Done({amout})')

    @commands.hybrid_command(name='kick', description='Кикает пользователя', with_app_command=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.hybrid_command(name='ban', description="Не банит пользователя", with_app_command=True)
    # @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(
            f"Бот подумал и пришел к выводу что {member.name} слишком хороший для бана и\nхочет чтобы вы использовали /kick (user)")

    async def sync_moder(self):
        await self.bot.tree.sync()


async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
