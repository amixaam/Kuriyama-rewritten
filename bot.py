import discord
from discord.ext import commands
import traceback
import json
import os

intents = discord.Intents.default()
client = commands.Bot(command_prefix='k', intents=intents)

with open(f"./json/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

@client.event
async def on_ready():
    await client.wait_until_ready()
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
    print(f'Logged in as {client.user} || v{settings["version"]}')
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(error)
    try:
        raise error
    except:
        er = traceback.format_exc()
        print(er)
        c = await client.fetch_channel(settings["traceback"])
        await c.send(f"``````py\n{er}\n``````")

client.run('NzgwMDIyMTIzMjg4NDYxMzEz.GzXiM8.ZXx3ncmqJ1oOmdLhX3_yOi3gKUMVF2v_s57aUw')
