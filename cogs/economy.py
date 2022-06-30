import discord
from discord.ext import commands
from Functions import *

class Economy(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command()
    async def profile(self, ctx):
        await ctx.send("profile");   

def setup(client):
    client.add_cog(Economy(client))