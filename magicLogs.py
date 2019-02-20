#░░░░░░░░▄▄▄▀▀▀▄▄███▄░░░░░░░░░░░░░░
#░░░░░▄▀▀░░░░░░░▐░▀██▌░░░░░░░░░░░░░
#░░░▄▀░░░░▄▄███░▌▀▀░▀█░░░░░░░░░░░░░
#░░▄█░░▄▀▀▒▒▒▒▒▄▐░░░░█▌░░░░░░░░░░░░
#░▐█▀▄▀▄▄▄▄▀▀▀▀▌░░░░░▐█▄░░░░░░░░░░░
#░▌▄▄▀▀░░░░░░░░▌░░░░▄███████▄░░░░░░
#░░░░░░░░░░░░▐░░░░▐███████████▄░░░
#░░Author:░░░░▐░░░░▐█████████████▄
#░░░Nathan░░░░░▀▄░░░▐█████████████▄
#░░░░░Fernandes░░░▀▄▄███████████████
#░░░░░░░░░░░░░░░░░░░░░░░░█▀██████░░

import discord
from os import listdir
from os.path import isfile, join
from discord.ext import commands

bot = commands.Bot(command_prefix="$", description="Manages OSRS stats for Discord")


# Unsure if I have made this properly
@bot.async_event
async def on_command_error(ctx, error):
    print("---\n"+str(error.message.channel)+"\n---")
    await bot.say('fetus deletus',str(error.message.channel))

@bot.event
async def on_ready():
    await LoadCogs()
    print('All cogs have been loaded')
    
async def LoadCogs():
        for extension in [f.replace(".py","") for f in listdir("cogs") if isfile(join("cogs",f))]:
            try:
                if not "__init__" in extension:
                    print("Loading {}...".format(extension),end='')
                    bot.load_extension("cogs." + extension)
            except Exception as e:
                print("Failed to load cog, {}".format(e))

def Main():
    botSecret = open("botSecret.txt","r")
    bot.run(botSecret.read())

if __name__ == "__main__":
    Main()