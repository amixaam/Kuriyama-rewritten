import discord, datetime, os
from discord.ext import commands
from Functions import *

class Helpful(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pingers: {round(self.client.latency * 1000)}ms')

    #owner commands
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send('loaded!')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.send('unloaded!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension = None):
        if (extension == None): #reload all cogs
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                    self.client.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send('reloaded!')
        else: #reload specific cog
            self.client.unload_extension(f'cogs.{extension}')
            self.client.load_extension(f'cogs.{extension}')
            await ctx.send('reloaded!')

def setup(client):
    client.add_cog(Helpful(client))