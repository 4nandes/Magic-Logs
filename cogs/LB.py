from discord.ext import commands
from discord import embeds
from lib.labels import labels
from lib.database import database

#Need to make sure that the leaderboard that is returned only contains the people that are in that particular server
#at the moment it grabs all of the people. There needs to be a for loop for the RSUN's that are in the server that the message came from
class LB:
    def __init__(self,bot):
        self.bot = bot
        self.labels = labels().getLabels()
        self.icons = labels().getIcons()

    @commands.command(pass_context=True)
    async def LB(self, ctx):
        data = " ".join(ctx.message.content.split(" ")[1:]).lower()
        if data == "":
            msg = database().highScores()
            emb = embeds.Embed(title="Server Leaderboard",description=msg, color=0x9b59b6)
            emb.set_thumbnail(url=self.icons[0])
            await ctx.bot.say(embed=emb)
            return
        try:
            msg = ""
            skillName = data.capitalize()
            data = database().leaderBoard(data)
            for x in range(0,len(data)):
                msg += "`" + data[x][0] + ("."*(20-len(data[x][0])))  + "Lvl: " + str(data[x][2]) +(" "*(4-len(str(data[x][2])))) + " XP: " + "{:,}`\n".format(int(data[x][1]))
            emb = embeds.Embed(title="{} Leaderboard:".format(skillName), description=msg, color=0x9b59b6)
            emb.set_thumbnail(url=self.icons[self.labels.index(skillName)])
            await ctx.bot.say(embed=emb)
            return
        except:
            await ctx.bot.say("That skill was not found")
            return

def setup(bot):
    bot.add_cog(LB(bot))
    print("LOADED")