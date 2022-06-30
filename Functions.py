import json
from operator import contains
import discord

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
    data[id] = await LoadJson("USERTEMPLATE")
    return data

async def UpdateUser(data, id):
    for key, value in data[id]["economy"]:
        if value < 0: data[id]["economy"]["key"] = 0
    
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
        return int(text.replace('m', '')) * 60 * 60 * 24

