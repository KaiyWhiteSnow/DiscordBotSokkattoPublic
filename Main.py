import discord
from discord.ext import commands
from discord.utils import get
import random
from random import randint
from rustplus import *
import asyncio
import time

#Main funstions
intents = discord.Intents.all()
client = discord.ext.commands.Bot(command_prefix="!", intents=intents)

socket = None

async def connect_rustapi():
    global socket
    socket = RustSocket()
    await socket.connect()
    socket.chat_event(chat)

    await socket.send_team_message(message="[BOT] Logged in as {0.user}. Waiting for further instructions.".format(client))

seconds = time.time()
localTime = time.ctime(seconds)

## Console - execute
@client.event
async def on_ready():
    await connect_rustapi()
    await client.tree.sync()
    print(localTime, "[BOT] INFO: We have logged in as {0.user}. Waiting for further instructions.".format(client))

#Commands Rust

async def chat(event : ChatEvent):
    if event.message.message == "!time":
        await socket.send_team_message(f"It is {(await socket.get_time()).time}")
        print(localTime, f"[BOT] INFO: Command !time has connected; Returning")
    elif event.message.message == "!smartSwitchOff":
        await socket.turn_off_smart_switch(553875739)
        print(localTime, f"[BOT] INFO: Command !smartSwitchOff has connected; Returning")
    elif event.message.message == "!smartSwitchOn":
        await socket.turn_on_smart_switch(553875739)
        print(localTime, f"[BOT] INFO: Command !smartSwitchOn has connected; Returning")
    elif event.message.message == "!dadJoke":
        i = random.randint(1, 5)
        if i == 1:
            await socket.send_team_message("Why do fathers take an extra pair of socks when they go golfing?\nIn case they get a hole in one!")
        elif i == 2:
            await socket.send_team_message("What do you call a fish wearing a bowtie?\nSofishticated.")
        elif i == 3:
            await socket.send_team_message("I'm afraid for the calendar. Its days are numbered.")
        elif i == 4:
            await socket.send_team_message("Dear Math, grow up and solve your own problems.")
        elif i == 5:
            await socket.send_team_message("What did Baby Corn say to Mama Corn?\nWhere's Pop Corn?")
        print(f"[BOT] INFO: Command !dadJoke has connected; Returning")
        return
    elif event.message.message == "!Quote":
        i = random.randint(1, 5)
        if i == 1:
            await socket.send_team_message(f"That guy above me is a goat")
        elif i == 2:
            await socket.send_team_message(f"私はペドファイルです")
        elif i == 3:
            await socket.send_team_message(f"All animals are equal, just some are more equal than others")
        elif i == 4:
            await socket.send_team_message(f"このなめるつま先の下の人")
        elif i == 5:
            await socket.send_team_message(f"69")
        print(localTime, f"[BOT] INFO: Command !Quote has connected; returning")
        return
    else:
        print(localTime, f"[Player] {event.message.name}: {event.message.message}")

## Restart command for discord
@client.command()
async def restart(ctx):
    await socket.send_team_message(f"{localTime}Restart - Bot will come up shortly, wait for confirmation message before using commands")
    

#Commands discord
## When is wipe
@client.command()
async def wheniswipe(ctx):
    await ctx.channel.send("Next wipe happens <t:1677783600:R>")
    print(localTime, "[BOT] INFO:Command !wheniswipe connected; returning")

## New leader
@client.command()
async def newLeader(ctx, steamID: int=""):
    await socket.promote_to_team_leader(steamID)
    print(localTime, "[BOT] INFO:Command !newLeader connected; returning")

## Time
@client.command()
async def time(ctx):
    await socket.send_team_message(f"It is {(await socket.get_time()).time}")

##Smart switch on
@client.command()
async def smartSwitchOn(ctx):
    await socket.turn_on_smart_switch(553875739)

## Smart switch off
@client.command()
async def smartSwitchOff(ctx):
    await socket.turn_off_smart_switch(553875739)

## Ping pong
@client.command()
async def ping(ctx):
	await ctx.channel.send("pong")
        
## Dad jokes
@client.command()
async def dadJoke(ctx):
    i = random.randint(1, 5)
    if i == 1:
        await ctx.channel.send("Why do fathers take an extra pair of socks when they go golfing?\nIn case they get a hole in one!")
    elif i == 2:
        await ctx.channel.send("What do you call a fish wearing a bowtie?\nSofishticated.")
    elif i == 3:
        await ctx.channel.send("I'm afraid for the calendar. Its days are numbered.")
    elif i == 4:
        await ctx.channel.send("Dear Math, grow up and solve your own problems.")
    elif i == 5:
        await ctx.channel.send("What did Baby Corn say to Mama Corn?\nWhere's Pop Corn?")
    print(localTime, f"[BOT] INFO: Command !dadJoke has connected; Returning")
    return

## Random quotes
@client.command()
async def quote(ctx):
    i = random.randint(1, 5)
    if i == 1:
        await ctx.channel.send(f"That guy above me is a goat")
    elif i == 2:
        await ctx.channel.send(f"私はペドファイルです")
    elif i == 3:
        await ctx.channel.send(f"All animals are equal, just some are more equal than others")
    elif i == 4:
        await ctx.channel.send(f"このなめるつま先の下の人")
    elif i == 5:
        await ctx.channel.send(f"69")
    print(localTime, f"[BOT] INFO: Command !Quote has connected; returning")
    return

## Repeat after me
@client.command()
async def say(ctx, text: str=""):
    await ctx.channel.send(text if text else "I got nothin' to say dawg")

## Help me
@client.command()
async def helpme(ctx):
    await ctx.channel.send("Hello, my name is Sokkatto. I'm a bot developed by Kaiy#3993. I was an old abandoned project from 2020, but later in 2023 Kaiy started working on me again and plans to frequently update me.")
    await ctx.channel.send("If youd like to see list of my commands please use !commands")

## Commands list
@client.command()
async def commands(ctx):
    await ctx.channel.send(f"!ping - Reply pong. ;)\n!quote - I will pick a random quote which I'll send to you.\n!say - After say you can put anything (or nothing?) and I'll say it.\n!helpme - Basic information\n!wheniswipe - I will tell you when wipe hits\n!dadJoke - Life is better with bad jokes innit?")
    print("[BOT] INFO: Command !commands has connected; returning")
    return

#On server join 
@client.event 
async def on_member_join(member):
    channel=client.get_channel()
    emb=discord.Embed(title="New member has joined",description=f"Thanks {member.mention} for being part of the bros!")
    await channel.send(embed=emb)
    print(localTime, "[BOT] INFO: {member.name} has joined the server; Following > RoleAsign".format(client))

#Adds role
    Server_ = client.get_guild({})
    if "YourRole" in (member.roles):
        return
    if not "YourRole" in str(member.roles):
        await member.add_roles(discord.utils.get(Server_.roles, name="YourRole"))
        print(localTime, "[BOT] INFO: {member.name} has been given role YourRole; Returning".format(client))

client.run("")