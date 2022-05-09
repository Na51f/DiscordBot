import discord
from discord.ext import commands
import music

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup()

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())
client.run('OTczMDc5NDY0NTMzNzA0NzI0.Gf2OG7.vu8uhOg8sQuH7zjMftRJSvw7G3pEmyJKOWfzJo')
