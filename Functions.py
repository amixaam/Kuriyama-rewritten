import json
import discord

async def loadjson(jsonname):
    with open(f"./json/{jsonname}.json", "r", encoding="utf-8") as f:
        return json.load(f)

async def dumpjson(jsonname, data):
    with open(f"./json/{jsonname}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

async def createembed(user = None):
    settings = await loadjson("Kuriyamasettings")
    economy = await loadjson("users")
    embed = discord.Embed()
    embed.set_footer(text=f"{settings['version']}")

    if user != None:
        if str(user.id) in economy:
            if economy[str(user.id)]['customization']['customcolor'] != None:
                embed.colour = economy[str(user.id)]['customization']['customcolor']
    return embed