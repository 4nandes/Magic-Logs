from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels

class register:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(register(bot))
    print("LOADED")