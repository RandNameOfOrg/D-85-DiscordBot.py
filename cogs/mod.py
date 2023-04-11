from . import Plugin
from core import Bot
from typing import Optional
import discord
from discord.ext import commands
from logging import getLogger, basicConfig; log = getLogger("Bot")

class Moderation(Plugin):
    def __init__(self, bot:Bot):
        self.bot=bot

    @commands.hybrid_command(name='clear', description='удаляют выбранное кол-во сообщений', with_app_command=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amout: int):
        await ctx.channel.purge(limit=(amout))
        await ctx.send(f'Done({amout})')

    @commands.hybrid_command(name='kick', description='Кикает пользователя', with_app_command=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))