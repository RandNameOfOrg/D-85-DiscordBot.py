import discord
from discord.ext import commands
from discord.ui import Button, View


class Vote(discord.ui.View):
    def __init__(self, *, title, timeout=100):
        super().__init__(timeout=timeout)
        self.title = 'test'


    @discord.ui.Button(style=discord.ButtonStyle.green, label="Accept", emoji="✅")
    async def TrueB(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{interaction.response.author.mention} принял голосование --> {self.title}')

    @discord.ui.Button(style=discord.ButtonStyle.danger, label="cancellation", emoji="❌")
    async def FalseB(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'{interaction.response.author.mention} не согласен с голосованием --> {self.title}')

    async def on_button_click(interaction):
        response = await bot.wait_for("button_click")
        name = voteIdTexts.get(response.message.id)
        if response.component.label == "Accept":
            await response.channel.send(response.author.mention + " принял,vote: " + name)
        else:
            await response.channel.send(response.author.mention + " не принял,vote: " + name)


class Button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vote(self, ctx, title: str, message: str):
        try:
            await ctx.send(discord.Embed(title=title, description=message, colour=discord.Colour.orange()), view=Vote())
        except:
            await ctx.send(embed=discord.Embed(description="используйте !vote [text] [message]", colour=discord.Color.red()))

async def setup(bot):
    await bot.add_cog(Button(bot=bot))