import discord
from discord.ext import commands
from datetime import *
import time
import random
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
        
        data = await UpdateUser(data, uid)
        embed = await CreateEmbed()
        embed.set_author(name=f"{await NamePrettier(user.display_name)} profile!")

        embedValue = ''
        for key, value in data[uid]['economy'].items():
            if key == "total": continue
            embedValue += f"{key}: `¥{value}`\n" 
        embed.add_field(name="Money", value=embedValue)

        embedValue = ''
        for key, value in data[uid]['timers'].items():
            embedValue += f"{key}: `{value}`\n" 
        embed.add_field(name="Timers", value=embedValue)

        #DEBUG
        settings = await LoadJson("settings")
        if str(ctx.author.id) in settings['debug']:
            if "debug" not in data[str(ctx.author.id)]: 
                data[str(ctx.author.id)]["debug"] = True
            if data[str(ctx.author.id)]["debug"] == True:
                embedValue = ''
                for key, value in data[uid].items():
                    embedValue += f"{key}: {value}\n"
                embed.description = embedValue

        await DumpJson("data", data)
        await ctx.send(embed=embed)

    @commands.command()
    async def daily(self, ctx):
        uid = str(ctx.author.id)
        settings = await LoadJson("settings")
        data = await LoadJson("data")
        data = await CreateUser(uid)
        if str(date.today().day) == data[uid]['timer']['daily']: #if it is the same day
            tomorrow = date.today() + timedelta(1)
            midnight = datetime.combine(tomorrow, time.time())
            now = datetime.now()
            return (midnight - now).seconds
            return await ctx.send("wait for " + await SecondsToText((midnight - datetime.now()).seconds - datetime.now()))
        
        dailyValue = int(1000 * (random.randrange(10, 14) / 10)) #up to a 1.4% bonus
        data[uid]['timer']['daily'] = str(date.today().day)
        data[uid]['economy']['pockets'] += dailyValue
        data[uid]['statistic']['daily']['times'] += 1
        data[uid]['statistic']['daily']['earned'] += dailyValue

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send("doned!")

def setup(client):
    client.add_cog(Economy(client))