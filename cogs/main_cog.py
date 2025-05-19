import asyncio
import datetime
import os
import os.path

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from core import Bot, Embed
from . import Plugin

# import functools, typing, asyncio
# import App #Disabled

__all__ = (
    "Main",
    "setup",
)


class VoteView(discord.ui.View):
    def __init__(self, title: str, timeout: int, max_users: int = 0, author: discord.User = None):
        super().__init__()
        self.title = title
        self.timeout = timeout
        self.embed = None
        if max_users != 0:
            self.max_users = max_users
        else:
            self.max_users = None
        self.data = {"accepted": 0, "canceled": 0, "users": 0}
        self.__golos = []
        self.__buttons = []
        self.__author = author
        self._message: discord.Message | None = None

    @discord.ui.button(label="Accept", emoji="✅", style=discord.ButtonStyle.green)
    async def accept(self, interaction: Interaction, button: discord.ui.Button):
        if button not in self.__buttons:
            self.__buttons.append(button)

        if self.interacted(interaction):
            await interaction.response.send_message(f'Вы уже участвовали в голосовании {self.title}', ephemeral=True)

        self.data["accepted"] += 1
        self._update()
        await interaction.response.send_message(f'Вы приняли {self.title}', ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.red, label="cancel", emoji="❎")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if button not in self.__buttons:
            self.__buttons.append(button)
        if self.interacted(interaction):
            await interaction.response.send_message(f'вы уже участвовали в голосовании {self.title}', ephemeral=True)

        self.data["canceled"] += 1
        self._update()
        await interaction.response.send_message(f'Вы отказались от {self.title}', ephemeral=True)

    def interacted(self, interaction: Interaction) -> bool:
        self._update()
        if interaction.user in self.__golos:
            return True

        self.__golos.append(interaction.user)
        return False

    def _update(self):
        self.data["users"] = self.data["accepted"] + self.data["canceled"]
        if self.max_users is not None:
            if self.data["users"] >= self.max_users:
                self.stop_vote()

    def stop_vote(self):
        for btn in self.__buttons:
            btn.disabled = True
        self.embed = Embed(title=self.title, description=f'Голосование завершено')
        self.embed.set_footer(text=f'Всего участников: {self.data["users"]}')
        self.embed.add_field(name='Приняли голосование', value=f'{self.data["accepted"]}')
        self.embed.add_field(name='Отказались от голосования', value=f'{self.data["canceled"]}')
        self.embed.set_author(name=self.__author.name, icon_url=self.__author.display_avatar.url)
        asyncio.get_running_loop().create_task(self._message.edit(embed=self.embed, view=None))


# noinspection PyUnresolvedReferences
class Main(Plugin):
    def __init__(self, bot: Bot, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)
        self.bot = bot
        self.profiles = os.path.abspath(__file__).replace("main_cog.py", "cogs\\")
        loop = asyncio.get_running_loop()
        loop.create_task(self.sync_code())

    async def sync_code(self):
        await self.bot.tree.sync()

    # region commands
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = Embed(
            title="Error:",
            description=f"```{error}```",
        )
        await ctx.reply(embed=embed, ephemeral=True)

    @app_commands.command(name='date', description='date')
    async def date(self, interaction: Interaction):
        now = datetime.datetime.now(datetime.timezone.utc)
        await interaction.response.send_message(now.strftime("сейчас %d.%m.%y %H:%M:%S UTC"))

    @app_commands.command(name='test_command', description='Beta-command (unstable)')
    async def test_command(self, interaction: Interaction):
        await interaction.response.send_message("<:404:1166453427723841536>")

    @app_commands.command(name='vote', description='Голосование')
    async def vote(self, interaction: Interaction, title: str, timeout: int = 600, max_users: int | None = None):
        view = VoteView(title=title, timeout=timeout, max_users=max_users, author=interaction.user)
        embed = Embed(title=title)
        embed.set_author(name=f"by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        msg = await interaction.channel.send(embed=embed, view=view)
        if msg is None:
            await interaction.response.send_message(f'Не удалось создать голосование', ephemeral=True)
            return
        await interaction.response.send_message(f'Голосование создано', view=admin_view, ephemeral=True)
        view._message = msg

    # endregion


async def setup(bot: Bot):
    await bot.add_cog(Main(bot))
