import json
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
