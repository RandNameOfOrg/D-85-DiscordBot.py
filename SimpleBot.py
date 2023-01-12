from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#import cogs.file.reload as rl
from discord.ext import commands, tasks
#from discord_components import DiscordComponents, Button, ButtonStyle
from discord.utils import get
from discord.ui import Button, View
import os, sys, json, discord, datetime, asyncio
from cogs import help, events

profiles = "cogs/file/"
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
voteIdTexts = {}

with open(profiles + '\\chlog.txt', 'r') as f:
    console = bot.get_channel(int(f.readline(100)))
    f.close()

if not os.path.exists(profiles + '\\users.json'):
    with open(profiles + '\\users.json', 'w') as file:
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


@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, am: int):
    await ctx.channel.purge(limit=am)

@bot.command()
async def reload(ctx):
    try:
        rl.reload()
        await ctx.send(embed = discord.Embed(description="Успешно!", colour=discord.Color.green()))
    except:
        await ctx.send(embed=discord.Embed(description="Error! Сбой програмы", colour=discord.Color.red()))

@bot.command()
@commands.has_role("admin")
async def setreports(ctx, member: discord.Member, reason: str):
    if reason.lower() == "0" or reason.lower() == "1":
        set(member)

@bot.event
async def on_member_join(member):
    channel = client.get_channel(839807318162145290)

    role = discord.utils.get (member.guild.roles, id=839807022949335050)
    print ('user join the servers')
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'``{member.name}`` присоиединился', color = 0x0c0c0c))

@bot.command()
async def reloadcog(ctx, ext):
    if ctx.author.id == 849351619878715392:
        bot.unload_extension(f"Cogs.{ext}")
        bot.load_extension(f"Cogs.{ext}")
        await ctx.send("tesog reloaded")
    else:
        await ctx.send("1")


@bot.command()
async def report(ctx, member: discord.Member):

    with open(profiles + 'users.json', 'r') as file:
        data = json.load(file)
        if data[str(member.id)]['WARNS'] >= 4:
            await ctx.send(embed = discord.Embed(title="❗❗📣ВНИМАНИЕ📣❗❗", description=f"У {member.name} уже {data[str(member.id)]['WARNS'] + 1} Жалоб!!!", colour=discord.Color.red()))
        file.close()

    with open(profiles + 'users.json', 'w') as file:
        data[str(member.id)]['WARNS'] += 1
        json.dump(data, file, indent=6)
        file.close()
    await ctx.send(embed=discord.Embed(title="Жалоба отправлена.", colour=discord.Color.dark_gray))

@bot.command()
async def setlog(ctx, id):
    try:
        print("Новое Id: " + id)
        f = open(profiles + 'chlog.txt', 'w')
        f.write("" + id)
        f.close()
        console = bot.get_channel(id)
        await ctx.send(embed = discord.Embed(description="Успешно! Оповещение о включении будет изменено после перезагрузки", colour=discord.Color.green()))
    except:
        await ctx.send(embed = discord.Embed(description="Error! неверное ID или сбой програмы", colour=discord.Color.red()))

@bot.command()
async def vote(ctx,*,title):
    try:
        msg= await ctx.send(
            embed=discord.Embed(title=title),
            components=[
                Button(style=ButtonStyle.green,label="Accept",emoji="✅"),
                Button(style=ButtonStyle.red, label="cancellation", emoji="❌")
            ]
        )
        voteIdTexts.update({msg.id:title})
    except:
        await ctx.send(embed = discord.Embed(description="используйте !vote [text]", colour=discord.Color.red()))

@bot.event
async def on_button_click(interaction):
    response = await bot.wait_for("button_click")
    name = voteIdTexts.get(response.message.id)
    if response.component.label == "Accept":
        await response.channel.send(response.author.mention + " принял,vote: " + name)
    else:
        await response.channel.send(response.author.mention + " не принял,vote: " + name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("команда использована не правильно")
    elif isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingPermissions):
        await ctx.send("")

@bot.command()
@commands.has_role('Python Developer')
async def unreport(ctx, mem: discord.Member):
    if ctx.author.id == 849351619878715392:
        await ctx.delete()
        with open(profiles + "users.json", "r") as file:
            data = json.load(file)
            file.close()
        with open(profiles + 'users.json', 'w') as file:
            data[str(mem.id)]['WARNS'] -= 1
            json.dump(data, file, indent=6)
            file.close()
        await ctx.send('Успешно!')
    else:
        await ctx.send("Пользователь не вертифицырован!!")

@bot.command()
async def bd(ctx, user):
   enter = bd_enter(user)
   await ctx.send(enter)

def bd_enter(user):
   for i in range(len(users)):
       if user == usersId[i]:
           enter = user + users[i]
       else:
           if user == botsId[i]:
               enter = user + " обнаружен в базе... это - " + bots[i]
           else:
               enter = "Ошибка! User не найден. Использование !bd user#0000"
           return enter



@bot.command()
async def date(ctx):
    now = datetime.datetime.now()
    await ctx.send(now.strftime("сейчас %y.%m.%d по МСК"))

@bot.command()
async def test_command(ctx):
    await ctx.send("тестовых команд пока нет😟😉 или вы о них не знаете🤐") \

@bot.command()
async def cat(ctx):
    await ctx.send("https://i.gifer.com/JtaW.gif")


@bot.command(name='dog', help='giv')
async def dog(ctx):
    await ctx.send("https://i.gifer.com/2g.gif")

@bot.command(help='perimeter')
async def perimeter(ctx,x,y):
    try:
        await ctx.send(int(x)*int(y))
    except:
        await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

@bot.command(help='3D cube')
async def cube(ctx,x,y,z):
    try:
        await ctx.send(int(x)*int(y)*int(z))
    except:
        await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))

@bot.command(name='difference', help='вычетание')
async def difference(ctx, w, y):
    try: await ctx.send(int(w) - int(y))
    except: await ctx.send(embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))


@bot.command(name='multiply', help='умножение')
async def multiply(ctx, w, y):
    try:
        await ctx.send(int(w) * int(y))
    except:
        await ctx.send(
            embed=discord.Embed(description="Используйте цифры", colour=discord.Color.red()))


@bot.command(name='divide', help='деление')
async def divide(ctx, w, y):
    if y=="0":
        await ctx.send("wes")
    else:
        await ctx.send(int(w) / int(y))


@bot.command(name='brush', help='сумма')
async def brush(ctx, w, y):
    await ctx.send(int(w) + int(y))


@bot.command(name='smile', help='эмодзи это-го сервера')
async def smile(ctx):
    await ctx.send("<:boteon:706935391852167208> ")


@bot.command(name='kick', help='КИКАЕТ')
@commands.has_role('admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

async def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            await bot.load_extension("cogs." + f[:-3])


if __name__ == "__main__":
    asyncio.run(main())
    bot.run("TOKEN")