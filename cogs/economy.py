import discord
from discord.ext import commands
from Functions import *
from datetime import *
import random

class Economy(commands.Cog):

    def __init__(self, client):
       self.client = client

    @commands.command(brief='See your progress', description="The only place to view and track your progress!")
    async def profile(self, ctx, user: discord.User=None):
        user = ctx.author if not user else user
        uid = str(user.id)
        data = await LoadJson("data")
        
        if uid not in data:
            if user == ctx.author: data = await CreateUser(uid)
            else: return await ctx.send("This user hasn't made a profile.")
        
        data = await UpdateUser(data, uid)
        embed = await CreateEmbed(data[uid]['settings']['sidecolor'])
        embed.set_author(name=f"{await NamePrettier(user.display_name)} profile!")

        embedValue = ''
        for key, value in data[uid]['economy'].items():
            if key == "total": continue
            embedValue += f"{key}: `{settings['currency'][0]}{value}`\n" 
        embed.add_field(name="Money", value=embedValue)

        embed.add_field(name="Streak", value=f"`{data[uid]['statistic']['daily']['streak']} days`")

        #DEBUG
        if str(ctx.author.id) in settings['debug']:
            if "debug" not in data[str(ctx.author.id)]["settings"]: 
                data[str(ctx.author.id)]["settings"]["debug"] = False
            if data[str(ctx.author.id)]["settings"]["debug"] == True:
                embedValue = ''
                for key, value in data[uid].items():
                    embedValue += f"{key}: {value}\n"
                embed.description = embedValue

        data[str(ctx.author.id)]["statistic"]["other"]["inventoryOpened"] += 1
        await DumpJson("data", data)
        await ctx.send(embed=embed)

    @commands.command(brief='Earn daily coins', description=f"Check in every day (0:00 EST) to claim your free daily {settings['currency'][1]} and continue your streak!\nRecieve a bonus between +0% and +40%")
    async def daily(self, ctx):
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        
        embed = await CreateEmbed()
        embed.title = ":gift:Daily reward!:gift:"

        if datetime.now().strftime('%d/%m/%Y') == data[uid]['timer']['daily']: #if it is the same day
            midnight = datetime.combine(datetime.now() + timedelta(days=1), time())
            embed.description = f"continue your streak in: `{await SecondsToText((midnight - datetime.now()).seconds)}`"
            embed.set_footer(text=f"streak: {data[uid]['statistic']['daily']['streak']}")
            return await ctx.send(embed=embed)
        
        #daily streak
        if (datetime.now() + timedelta(days=-1)).strftime('%d/%m/%Y') == data[uid]['timer']['daily']:
            embed.set_footer(text=f"streak: {data[uid]['statistic']['daily']['streak'] + 1}")
        else:
            if data[uid]['timer']['daily'] == 0: embed.set_footer(text="streak: 1")
            else: embed.set_footer(text="streak: 1 (streak lost!)")
            data[uid]['statistic']['daily']['streak'] = 0

        bonus = random.uniform(0, 0.4) #up to a 40% bonus
        dailyValue = int(1000 * (1 + bonus))
        data[uid]['timer']['daily'] = datetime.now().strftime('%d/%m/%Y')
        data = await ChangeBalance(data, uid, dailyValue)
        data[uid]['statistic']['daily']['times'] += 1
        data[uid]['statistic']['daily']['earned'] += dailyValue
        data[uid]['statistic']['daily']['streak'] += 1

        embed.add_field(name="Earned", value=f"`{settings['currency'][0]}{dailyValue} ({round(bonus*100)}% bonus!)`")

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send(embed=embed)

    @commands.command(brief='Gamble your money', description=f"Enter amount of {settings['currency'][1]} you wish to gamble (also can enter: 'half', 'h', 'all', 'a' instead of number).\nTotally a 50/50 chance to double or lose your money")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def gamble(self, ctx, amount = None):
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        
        if amount == None: return await ctx.send("Please enter an amount or an abbreviation!")
        amount = await AbreviationToInt(amount, data[uid]['economy']['pockets'])
        if (isstring(amount)): #if string, then it's an error
            return await ctx.send(amount)

        embed = await CreateEmbed()
        embed.title = ":game_die:Gamble!:game_die:"

        #gambling is *totally* 50/50
        if random.random() > 0.35: #lose
            gambleValue = amount * -1
            data[uid]['statistic']['gamble']['lost'] += gambleValue
            embed.add_field(name="Lost", value=f"`{settings['currency'][0]}{abs(gambleValue)}`")
            embed.colour = embedColors[1]
        else:
            gambleValue = (amount * 2) - amount
            data[uid]['statistic']['gamble']['earned'] += gambleValue
            embed.add_field(name="Earned", value=f"`{settings['currency'][0]}{abs(gambleValue + amount)}`")
            embed.colour = embedColors[0]

        data[uid]['statistic']['gamble']['times'] += 1
        data = await ChangeBalance(data, uid, gambleValue)

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send(embed=embed)

    @commands.group(brief="a set of commands relating to bank", description="see info about your bank stats")
    async def bank(self, ctx):
        if ctx.invoked_subcommand is not None: return
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        economy = data[uid]['economy']

        embed = await CreateEmbed()
        embed.title = ":sparkles:Kuriyama bank!:sparkles:"
        embed.description = "***the*** *place to keep your money safe!*"
        embed.add_field(name=":bank: Balance", value=f"bank: `{settings['currency'][0]}{economy['bank']}`")
        
        await ctx.send(embed=embed)

    @bank.command(brief=f'transfer {settings["currency"][1]}', description=f'transfer {settings["currency"][1]} from your bank to your pockets.\n(also can enter: "half", "h", "all", "a" instead of number).')
    async def deposit(self, ctx, amount = None):
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        
        embed = await CreateEmbed()
        embed.title = ":sparkles:Bank transfer!:sparkles:"
        embed.description = "*Thank you for using* ***Kuriyama Bank!***"

        bankbalance = data[uid]['economy']['bank']
        data = await TransferBalance(data, uid, amount, True)
        if isstring(data): return await ctx.send(data)

        economy = data[uid]['economy']
        embed.add_field(name=":bank: Bank", value=f"Balance: `{settings['currency'][0]}{economy['bank']} (+{settings['currency'][0]}{economy['bank']-bankbalance})`\n*Remainder in pockets: `{settings['currency'][0]}{economy['pockets']}`*")

        data[uid]['statistic']['bank']['times'] += 1
        data[uid]['statistic']['bank']['deposited'] += economy['bank'] - bankbalance

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send(embed=embed)
    
    @bank.command(brief=f'transfer {settings["currency"][1]}', description=f'transfer {settings["currency"][1]} from your bank to your pockets.\n(also can enter: "half", "h", "all", "a" instead of number).')
    async def withdraw(self, ctx, amount = None):
        uid = str(ctx.author.id)
        data = await LoadJson("data")
        data = await CreateUser(uid)
        data = await UpdateUser(data, uid)
        
        embed = await CreateEmbed()
        embed.title = ":sparkles:Bank transfer!:sparkles:"
        embed.description = "*Thank you for using* ***Kuriyama Bank!***"

        pocketBalance = data[uid]['economy']['pockets']
        data = await TransferBalance(data, uid, amount, False)
        if isstring(data): return await ctx.send(data)

        economy = data[uid]['economy']
        embed.add_field(name=":moneybag: Pockets", value=f"Balance: `{settings['currency'][0]}{economy['pockets']} (+{settings['currency'][0]}{economy['pockets']-pocketBalance})`\n*Remainder in bank: `{settings['currency'][0]}{economy['bank']}`*")

        data[uid]['statistic']['bank']['times'] += 1
        data[uid]['statistic']['bank']['withdrawn'] += economy['pockets'] - pocketBalance

        data = await UpdateUser(data, uid)
        await DumpJson("data", data)
        await ctx.send(embed=embed)

    @commands.command(brief='Remove your data', description="enter CONFIRM to remove your data")
    async def deleteprofile(self, ctx, confirm = None):
        data = await LoadJson("data")
        uid = ctx.author.id

        if str(uid) not in data:
            return await ctx.send("You do not own a profile")

        if confirm != "CONFIRM":
            return await ctx.send(f"If you wish to delete all data from your Kuriyama profile, type `{settings['prefix'][0]}deleteprofile CONFIRM`.\nYou can not reverse this action.")
        
        data = data.pop(uid, None)
        await DumpJson("data", data)
        await ctx.send(f"Data of {ctx.author} has been removed.")

def setup(client):
    client.add_cog(Economy(client))