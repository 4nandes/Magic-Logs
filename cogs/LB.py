from discord.ext import commands
from lib.labels import labels
from lib.database import database

#Need to make sure that the leaderboard that is returned only contains the people that are in that particular server
#at the moment it grabs all of the people. There needs to be a for loop for the RSUN's that are in the server that the message came from
class LB:
    def __init__(self,bot):
        self.bot = bot
        self.labels = labels().getLabels()

    @commands.command(pass_context=True)
    async def LB(self, ctx):
        data = " ".join(ctx.message.content.split(" ")[1:])
        if data == "":
            await ctx.bot.say("THIS IS NOT YET IMPLEMENTED")
            return
        try:
            data = data.capitalize()
            self.labels.index(data)
            msg = "**{} Leaderboard:**".format(data)
            data = data.lower()
            data = database().leaderBoard(data)
            for x in range(0,len(data)):
                msg += "\n`" + data[x][0] + ("."*(20-len(data[x][0])))  + "Lvl: " + str(data[x][2]) +(" "*(4-len(str(data[x][2])))) + " XP: " + "{:,}`".format(int(data[x][1]))
            await ctx.bot.say(msg)
            return
        except:
            await ctx.bot.say("That skill was not found")
            return

def setup(bot):
    bot.add_cog(LB(bot))
    print("LOADED")