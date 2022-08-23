import discord
import os
import asyncio
import pytz
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")
DAD_JOKE_API = os.getenv("DAD_JOKE_API")
IP_GEOLOCATION_API = os.getenv("IP_GEOLOCATION_API")


act = discord.CustomActivity("Listening to commands")
bot = commands.Bot(command_prefix="!")


def find_hcf(a, b):
    if b == 0:
        return a
    else:
        return find_hcf(b, a % b)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.command(help="Says hello to the user")
async def hello(ctx):
    user = ctx.author
    name = user[slice(user.index("#"))]
    await ctx.send(f"Hello, {name}!")


@bot.command(name="uktime", help="Get current time in uk")
async def uktime(ctx):
    timezone = pytz.timezone("GB")
    uk_time = datetime.now(timezone)
    current_uk_time = uk_time.strftime("%H:%M:%S")
    await ctx.send(f"Current Time in UK: {current_uk_time}")


@bot.command(help="Find hcf of two or more numbers")
async def hcf(ctx, *args: int):
    num1 = args[0]
    num2 = args[1]
    hcf = find_hcf(num1, num2)
    if len(args) > 2:
        for i in range(2, len(args)):
            hcf = find_hcf(hcf, args[i])
    await ctx.send(hcf)


@bot.command(help="Dad jokes")
async def dadjoke(ctx):
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        "X-RapidAPI-Key": DAD_JOKE_API,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    setup = json_data["body"][0]["setup"]
    punchline = json_data["body"][0]["punchline"]
    await ctx.send(setup)
    await asyncio.sleep(5)
    await ctx.send(punchline)


@bot.command(help="Get a random riddle followed by an answer after 10 seconds")
async def riddle(ctx):
    url = "https://riddles-api.vercel.app/random"
    response = requests.get(url)
    json_data = json.loads(response.text)
    riddle = json_data["riddle"]
    answer = json_data["answer"]
    await ctx.send(riddle)
    await asyncio.sleep(10)
    await ctx.send(answer)


@bot.command(help="get current time")
async def time(ctx):
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=" + IP_GEOLOCATION_API
    response = requests.get(url)
    json_data = json.loads(response.text)
    print(json_data)
    time = json_data["time_zone"]["current_time"]
    await ctx.send("current time: " + time[:19])


@bot.command(
    case_insensitive=True,
    aliases=["remind", "remindme", "remind_me"],
    help="Reminds you after a specified time",
)
# @commands.bot_has_permissions(attach_files=True, embed_links=True)
async def reminder(ctx, time, *, reminder=None):
    user = ctx.author
    embed = discord.Embed(colour=0xFFA500)
    seconds = 0
    if reminder is None:
        embed.add_field(
            name="Error",
            value="Usage: !remindme [time] [message]",
        )

    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    elif time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"

    if seconds < 60:
        embed.add_field(
            name="Error",
            value="You have specified a too short duration!\nMinimum duration is 1 minute.",
        )
    elif seconds > 7776000:
        embed.add_field(
            name="Error",
            value="You have specified a too long duration!\nMaximum duration is 90 days.",
        )
    else:
        await ctx.send(f'Alright, I will remind you about "{reminder}" in {counter}.')
        await asyncio.sleep(seconds)
        await ctx.send(
            f'Hey, {user.mention} you told me to remind you about "{reminder}" {counter} ago.'
        )
        return
    await ctx.send(embed=embed)


@reminder.error
async def reminder_error(ctx, error):
    error_embed = discord.Embed(colour=0xFF0000)
    if isinstance(error, commands.UserInputError):
        error_embed.add_field(name="Error", value="Usage: !remindme [time] [message]")
        await ctx.send(embed=error_embed)


bot.run(TOKEN)
