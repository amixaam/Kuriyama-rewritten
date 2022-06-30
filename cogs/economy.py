from email import message
import discord
from discord.ext import commands
from Functions import *

class Economy(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command()
    async def profile(self, ctx):
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        if uid not in data:
            data = await CreateUser(uid)
            
        embed = await CreateEmbed()
        embed.set_author(name="Your profile!")
        embed.description = data[uid]["economy"]["total"]
        await ctx.send(embed=embed)
        await DumpJson("data", data)

def setup(client):
    client.add_cog(Economy(client))