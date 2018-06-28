from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels

class LB:
    def __init__(self,bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(LB(bot))
    print("LOADED")