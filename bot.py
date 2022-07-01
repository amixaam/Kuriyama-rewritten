import discord
from discord.ext import commands, tasks
import traceback
from itertools import cycle
import json
import os

from Functions import CreateEmbed

with open(f"./json/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

intents = discord.Intents.default()
client = commands.Bot(command_prefix=settings["prefix"], intents=intents)


@client.event
async def on_ready():
    await client.wait_until_ready()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    print(f'Logged in as {client.user} || {settings["version"]}')
    global status
    status = cycle(['kuri help'])    
    change_status.start()

    embed = await CreateEmbed()
    embed.title="Beta test <:miraiwink:835613259423678484>"
    embed.description="Beta test open! <:miraiwink:835613259423678484><:miraiwink:835613259423678484><:miraiwink:835613259423678484>\n\n**I may be offline at times and some commands or saved data may break!**"
    channel = client.get_channel(settings['startup'])
    await channel.send(embed=embed)

@tasks.loop(seconds=10)
async def change_status():
    nextStatus = next(status)
    await client.change_presence(activity=discord.Activity(name=nextStatus, type=discord.ActivityType.playing))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("This command doesen't exist!")
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("Please pass in all required arguments!")
    if isinstance(error, commands.MemberNotFound):
        return await ctx.send("Member not found!")
        
    await ctx.send(error)
    try:
        raise error
    except:
        er = traceback.format_exc()
        print(er)
        c = await client.fetch_channel(settings['traceback'])
        await c.send(f"``````py\n{er}\n``````")

client.run(settings['token'])
