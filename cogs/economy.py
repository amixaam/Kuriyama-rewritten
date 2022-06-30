from email import message
import discord
from discord.ext import commands
from Functions import *

class Economy(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command()
    async def profile(self, ctx):
        user = ctx.author
        data = await LoadJson("data")
        if user.id not in data:
            await CreateUser(user)

        await ctx.send("profile")
        await DumpJson("data", data)

def setup(client):
    client.add_cog(Economy(client))