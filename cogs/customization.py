import discord
from discord.ext import commands
from Functions import *

class Customization(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.group(brief="a set of commands relating to profile customization")
    async def customize(self, ctx):
        if ctx.invoked_subcommand is not None: return
        await ctx.send('Check the `help customize` command for sub command info!')

    @customize.command(brief="customize your profile side-color!", description="customize your profile side-coolor by entering a color value you like!")
    async def color(self, ctx, colorValue): 
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        
        embed = await CreateEmbed()
        embed.title = "Side-color"

        try:
            colorValue = colorValue.replace("#", "0x")
            colorValue = int(colorValue,16)
        except:
            return await ctx.send("Hex values are supported!")

        embed.description = f"Side color changed to {colorValue}!"
        data[uid]['settings']['sidecolor'] = colorValue
        embed.colour = colorValue

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Customization(client))