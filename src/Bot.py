import discord
import random
import requests
import calendar
import datetime
from discord.ext import commands
import imdb
from typing import Optional


# create your bot class
class CONFING:
    TOKEN = 'TOKEN'
    PREFIX = '?'


client = commands.Bot(command_prefix=CONFING.PREFIX)
color = [0xC40B9C, 0x0B64C4, 0x11DC1F, 0xff4000, 0xbfff00, 0x00bfff, 0xff0000]


@client.event
async def on_ready():  # this part is OK
    servers = len(client.guilds)
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1

    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'{servers} servers and {members} members'
    ))
    print("Bot Online....")


# bot says that the command was not found
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        Embed_message = discord.Embed(
            title='Command Not Found',
        )
        Embed_message.set_image(url='https://cdn.iconscout.com/icon/premium/png-512-thumb/search-not-found-2344589'
                                    '-1965053.png')
        await ctx.send(embed=Embed_message)


# kick command
@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


# ban command
@client.command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


# unban command
@client.command()
@commands.has_permissions(manage_messages=True)
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    bans = await ctx.guild.bans()
    for i in bans:
        if user in i:
            await guild.unban(user=user)
            await ctx.send(f'{user.mention} Successfully Unbanned From Server')


# show bot information
@client.command()
async def info(ctx):
    global color
    Embed_message = discord.Embed(
        title='central bot',
        description="Crown Bot is kernel of this server",
        colour=random.choice(color)
    )
    Embed_message.set_image(url='https://i.pinimg.com/originals/cd/f0/9b/cdf09b00aea778cb509aafc4cccc4e77.png')
    await ctx.send(embed=Embed_message)


# create poll
@client.command()
@commands.has_permissions()
async def poll(ctx, question, *options: str):
    if len(options) > 2:
        await ctx.send('```Error! Syntax = [~poll "question" "option1" "option2"] ```')
        return

    if len(options) == 2 and options[0] == "yes" and options[1] == "no":
        reactions = ['👍', '👎']
    else:
        reactions = ['👍', '👎']

    description = []
    for x, option in enumerate(options):
        description += f'\n {reactions[x]} {option}'

    poll_embed = discord.Embed(title=question, color=0x31FF00, description=''.join(description))

    react_message = await ctx.send(embed=poll_embed)

    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)


api_key = 'api_key'
base_url = 'http://api.openweathermap.org/data/2.5/weather?'


# Show weather
@client.command(help="Show weather")
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Weather in {city_name}",
                                  color=ctx.guild.me.top_role.color,
                                  timestamp=ctx.message.created_at, )
            embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
            embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("City not found.")


# Show Time
@client.command(help='Show Time')
async def time(ctx):
    Embed_message = discord.Embed(
        title='Time',
        description=datetime.datetime.now().strftime("%H:%M:%S"),
        color=random.choice(color))
    Embed_message.set_footer(text=f"Requested by {ctx.author.name}")
    Embed_message.set_image(url='https://cdn4.iconfinder.com/data/icons/business-vol-4-4/96/Clock-512.png')
    await ctx.send(embed=Embed_message)


# Show Calendar
@client.command(help="Show Calendar")
async def Calendar(ctx, year: int, month: int):
    global color
    Embed_message = discord.Embed(
        title=f'calendar {year} {month}',
        description=calendar.month(year, month),
        color=random.choice(color)
    )
    Embed_message.set_footer(text=f"Requested by {ctx.author.name}")
    Embed_message.set_image(url='https://cdn4.iconfinder.com/data/icons/small-n-flat/24/calendar-512.png')
    await ctx.send(embed=Embed_message)


# Show server information
@client.command(name='server',
                help="Show server information")
async def ServerInfo(ctx):  # This part is OK
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    ID = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    Embed_message = discord.Embed(
        title=name + "Information",
        description=description,
        color=discord.Color.blue()
    )
    Embed_message.set_thumbnail(url=icon)
    Embed_message.set_image(url='https://cdn.iconscout.com/icon/premium/png-512-thumb/server-info-1103498.png')
    Embed_message.add_field(name="Owner", value=owner, inline=True)
    Embed_message.add_field(name="Server ID", value=ID, inline=True)
    Embed_message.add_field(name="Region", value=region, inline=True)
    Embed_message.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=Embed_message)


# Show User Information
@client.command(name="userinfo", help="Show User Information")
async def user_info(Ctx, Target: Optional[discord.Member]):
    if Target is None:
        Target = Ctx.author

    header = f"User information - {Target.display_name}\n\n"
    rows = {
        "Account name": Target.name,
        "Disciminiator": Target.discriminator,
        "ID": Target.id,
        "Is bot": "Yes" if Target.bot else "No",
        "Top role": Target.top_role,
        "Nº of roles": len(Target.roles),
        "Current status": str(Target.status).title(),
        "Current activity": f"{str(Target.activity.type).title().split('.')[1]} {Target.activity.name}" if Target.activity is not None else "None",
        "Created at": Target.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        "Joined at": Target.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
    }
    table = header + "\n".join(
        [f"{key}{' ' * (max([len(key) for key in rows.keys()]) + 2 - len(key))}{value}" for key, value in rows.items()])
    await Ctx.send(f"```{table}```{Target.avatar_url}")
    return


# set your bot's status
@client.command()
@commands.has_permissions()
async def status(ctx, status_type):  # This part is OK
    if status_type == "idle":
        await client.change_presence(status=discord.Status.idle)
        await ctx.send("Status changed to idle")
    elif status_type == 'dnd':
        await client.change_presence(status=discord.Status.dnd)
        await ctx.send("Status changed to dnd")
    else:
        await client.change_presence(status=discord.Status.online)
        await ctx.send("Status changed to online")


# set your bot's activity
@client.command(help='Show Activity')
@commands.has_permissions()
async def activity(ctx, activity_type, *, activity_text):  # This part is OK
    if activity_type == "listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                               name=activity_text))
        await ctx.send("Status changed")

    elif activity_type == "watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name=activity_text))
        await ctx.send("Status changed")

    elif activity_type == "playing":
        await client.change_presence(activity=discord.Game(name=activity_text))
        await ctx.send("Status changed")

    elif activity_type == "streaming":
        await client.change_presence(activity=discord.Streaming(name=activity_text,
                                                                url='https://www.twitch.tv/twitch'))
        await ctx.send("Status changed")
    else:
        await ctx.send("I can not read your command")


@client.command(pass_context=True, help='Show ping')
async def ping(ctx):
    global color
    pong = {round(client.latency * 1000)}
    Embed_message = discord.Embed(
        title=f'Ping is {pong} ms',
        colour=random.choice(color)
    )
    Embed_message.set_image(url='https://p.kindpng.com/picc/s/438-4387212_ping-logo-ping-png-transparent-png.png')
    await ctx.send(embed=Embed_message)


# clear all of message in text channel
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, count):
    count = int(count)
    await ctx.channel.purge(limit=count + 1)


# Show avatar
@client.command(help="Show avatar")
async def avatar(ctx, *, avamember: discord.Member = None):
    Embed_message = discord.Embed(
        title='show user avatar',
        color=random.choice(color)
    )
    Embed_message.set_image(url=avamember.avatar_url)
    Embed_message.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=Embed_message)


# Show Best movies
@client.command(name='Top', help="Show Best movies")
async def Top250Movies(ctx, count: int):
    ai = imdb.IMDb()
    movie = ai.get_top250_movies()

    for i in range(1, count + 1):
        Embed_message = discord.Embed(
            title='Top 250 movies',
            description=f"{i}==>>>{movie[i]['title']}",
            color=random.choice(color)
        )
        Embed_message.set_image(url='https://i.redd.it/gkfygy4k3tr21.jpg')
        Embed_message.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=Embed_message)


# lock channel
@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " ***is now in lockdown.***")


# unlock channel
@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")


# join to voice channel
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


# leave to voice channel
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# Slaps a member
@client.command(name="slap", help="Slaps a member")
async def slap_member(Ctx, Target: discord.Member):
    """Slaps a member."""
    await Ctx.send(f"**{Ctx.author.display_name}** just slapped {Target.mention} silly!")
    return


# run your bot
client.run(CONFING.TOKEN)