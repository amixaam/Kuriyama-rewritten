import json
import datetime
from math import floor
import discord

embedColors = [0x8cffab, 0xff7875]

async def LoadJson(jsonname):
    with open(f"./json/{jsonname}.json", "r", encoding="utf-8") as f:
        return json.load(f)

async def DumpJson(jsonname, data):
    with open(f"./json/{jsonname}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def CreateEmbed():
    economy = await LoadJson("data")
    embed = discord.Embed()
    #to be added: side color
    return embed

async def CreateUser(id):
    data = await LoadJson("data")
    if id not in data:
        data[id] = await LoadJson("USERTEMPLATE")
        return data
    return data

async def UpdateUser(data, id):
    economy = data[id]["economy"]
    for key, value in economy.items():
        if value < 0: economy[key] = 0
    
    economy['total'] = economy['pockets'] + economy['bank']
    return data
    
async def NamePrettier(text):
    if (text[-1] == 's'): return text + "'"
    else: return text + "'s"

async def TextToSeconds(text): #can only do 1 so far
    if "s" in text:
        return int(text.replace('s', ''))
    elif "m" in text:
        return int(text.replace('m', '')) * 60
    elif "h" in text:
        return int(text.replace('h', '')) * 60 * 60
    elif "d" in text:
        return int(text.replace('d', '')) * 60 * 60 * 24

async def SecondsToText(seconds):
    return str(datetime.timedelta(seconds=seconds))

async def AbreviationToInt(text, amount):
    half = ["half", "h"]
    all = ["all", "a"]

    text = text.lower()
    if text in half:
        return floor(amount / 2)
    elif text in all:
        return amount
    else:
        try:
            if int(text) > amount:
                return f"Cannot enter a number above your total {amount}"
            elif int(text) <= 0:
                return "Cannot enter a number smaller or equal to 0."
            else:
                return int(text)
        except:
            return f"Supported short words: {half}, {all}. Please use full numbers or these words!"

async def changeBalance(data, id, amount): #for easier transaction stuff
    economy = data[id]['economy']
    if (amount >= 0 ):
        economy['pockets'] += amount
        economy['net'] += amount
        return data
    
    economy['pockets'] += amount
    return data
        
