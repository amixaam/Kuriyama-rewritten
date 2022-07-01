from distutils.log import debug
import discord, datetime, os
from discord.ext import commands
from Functions import *

class Helpful(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command(brief='check ping')
    async def ping(self, ctx):
        await ctx.send(f'pingers: {round(self.client.latency * 1000)}ms')

    @commands.command(brief='debug purpouses')
    async def debug(self, ctx):
        settings = await LoadJson("settings")
        data = await LoadJson("data")
        uid = str(ctx.author.id)

        if uid in settings["debug"]:
            if "debug" not in data[uid]["settings"]:
                data[uid]["settings"]["debug"] = False
            data[uid]["settings"]["debug"] = not data[uid]["settings"]["debug"]
            await DumpJson("data", data)
            return await ctx.send(f'debug turned {data[uid]["settings"]["debug"]}')
        await ctx.send("no permission")

    #owner commands
    @commands.command(brief='debug purpouses')
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send('loaded!')

    @commands.command(brief='debug purpouses')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.send('unloaded!')

    @commands.command(brief='debug purpouses')
    @commands.is_owner()
    async def reload(self, ctx, extension = None):
        if (extension == None): #reload all cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                    self.client.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send('all cogs reloaded!')
        else: #reload specific cog
            self.client.unload_extension(f'cogs.{extension}')
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} reloaded!')

def setup(client):
    client.add_cog(Helpful(client))