import discord
from discord.ext import commands
import random
from rustplus import *
import time
from typing import Union
import config

# Main functions
intents = discord.Intents.all()
client = discord.ext.commands.Bot(command_prefix="!", intents=intents)

socket: Union[RustSocket, None] = None


async def connect_rustapi():
    global socket
    socket = RustSocket()
    await socket.connect()
    socket.chat_event(chat)

    await socket.send_team_message(
        message="[BOT] Logged in as {0.user}. Waiting for further instructions.".format(client))


seconds = time.time()
localTime = time.ctime(seconds)


# Console - execute
@client.event
async def on_ready():
    await connect_rustapi()
    await client.tree.sync()
    print(localTime, "[BOT] INFO: We have logged in as {0.user}. Waiting for further instructions.".format(client))


# Commands Rust
async def chat(event: ChatEvent):
    message = event.message.message.lower()
    if message == "!time":
        await socket.send_team_message(f"It is {(await socket.get_time()).time}")
        print(localTime, f"[BOT] INFO: Command !time has connected; Returning")

    elif message == "!smartswitchoff":
        await socket.turn_off_smart_switch(config.smart_switch_id)
        print(localTime, f"[BOT] INFO: Command !smartSwitchOff has connected; Returning")

    elif message == "!smartswitchon":
        await socket.turn_on_smart_switch(config.smart_switch_id)
        print(localTime, f"[BOT] INFO: Command !smartSwitchOn has connected; Returning")

    elif message == "!dadjoke":
        await socket.send_team_message(random.choice(config.dad_jokes))
        print(f"[BOT] INFO: Command !dadJoke has connected; Returning")
        return

    elif message == "!quote":
        await socket.send_team_message(random.choice(config.quotes))
        print(localTime, f"[BOT] INFO: Command !Quote has connected; Returning")
        return
    else:
        print(localTime, f"[Player] {event.message.name}: {event.message.message}")


# Restart command for discord
@client.command()
async def restart(ctx):
    await socket.send_team_message(
        f"{localTime}Restart - Bot will come up shortly, wait for confirmation message before using commands")


# Commands discord
# When is wipe
@client.command()
async def wheniswipe(ctx):
    await ctx.channel.send("Next wipe happens <t:1677783600:R>")
    print(localTime, "[BOT] INFO:Command !wheniswipe connected; returning")


# New leader
@client.command()
async def newLeader(ctx, steamID: int = ""):
    await socket.promote_to_team_leader(steamID)
    print(localTime, "[BOT] INFO:Command !newLeader connected; returning")


# Time
@client.command()
async def time(ctx):
    await socket.send_team_message(f"It is {(await socket.get_time()).time}")


# Smart switch on
@client.command()
async def smartSwitchOn(ctx):
    await socket.turn_on_smart_switch(config.smart_switch_id)


# Smart switch off
@client.command()
async def smartSwitchOff(ctx):
    await socket.turn_off_smart_switch(config.smart_switch_id)


# Ping pong
@client.command()
async def ping(ctx):
    await ctx.channel.send("pong")


# Dad jokes
@client.command()
async def dadJoke(ctx):
    await ctx.channel.send(random.choice(config.quotes))
    print(localTime, f"[BOT] INFO: Command !dadJoke has connected; Returning")
    return


# Random quotes
@client.command()
async def quote(ctx):
    await ctx.channel.send(random.choice(config.quotes))
    print(localTime, f"[BOT] INFO: Command !Quote has connected; returning")
    return


# Repeat after me
@client.command()
async def say(ctx, text: str = ""):
    await ctx.channel.send(text if text else "I got nothin' to say dawg")


# Help me
@client.command()
async def helpme(ctx):
    await ctx.channel.send(
        "Hello, my name is Sokkatto. I'm a bot developed by Kaiy#3993. I was an old abandoned project from 2020, "
        "but later in 2023 Kaiy started working on me again and plans to frequently update me.")
    await ctx.channel.send("If you'd like to see list of my commands please use !commands")


# Commands list
@client.command()
async def commands(ctx):
    await ctx.channel.send("""!ping - Reply pong. ;)
!quote - I will pick a random quote which I'll send to you.
!say - After say you can put anything (or nothing?) and I'll say it.
!helpme - Basic information
!wheniswipe - I will tell you when wipe hits
!dadJoke - Life is better with bad jokes innit?
""")
    print("[BOT] INFO: Command !commands has connected; returning")
    return


# On server join
@client.event
async def on_member_join(member):
    channel = client.get_channel(config.on_member_join_channel)
    emb = discord.Embed(title="New member has joined",
                        description=f"Thanks {member.mention} for being part of the bros!")
    await channel.send(embed=emb)
    print(localTime, "[BOT] INFO: {member.name} has joined the server; Following > RoleAssign".format(client))

    # Adds role
    server_ = client.get_guild(config.guild_id)
    if config.role_name in member.roles:
        return
    if config.role_name not in str(member.roles):
        await member.add_roles(discord.utils.get(server_.roles, name="YourRole"))
        print(localTime, "[BOT] INFO: {member.name} has been given role YourRole; Returning".format(client))


if __name__ == "__main__":
    client.run(config.client_token)
