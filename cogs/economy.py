from email import message
import discord
from discord.ext import commands
from Functions import *

class Economy(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command()
    async def profile(self, ctx, user: discord.User=None):
        user = ctx.author if not user else user
        uid = str(user.id)
        data = await LoadJson("data")
        if uid not in data:
            if user == ctx.author: data = await CreateUser(uid)
            else: return await ctx.send("This user hasn't made a profile.")
            
        embed = await CreateEmbed()
        embed.set_author(name=f"{await NamePrettier(user.display_name)} profile!")

        embedValue = ''
        for key, value in data[uid]['economy'].items():
            if key == "total": continue
            embedValue += f"{key}: `¥{value}`\n" 
        embed.add_field(name="Money", value=embedValue)

        settings = await LoadJson("settings")
        if str(ctx.author.id) in settings['debug']: #debug stats
            if "debug" not in data[str(ctx.author.id)]: 
                data[str(ctx.author.id)]["debug"] = True
            if data[str(ctx.author.id)]["debug"] == True:
                embedValue = ''
                for key, value in data[uid].items():
                    embedValue += f"{key}: {value}\n"
                embed.description = embedValue

        await ctx.send(embed=embed)
        await DumpJson("data", data)

def setup(client):
    client.add_cog(Economy(client))