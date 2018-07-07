from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.database import database
from lib.labels import labels
from discord import embeds
import datetime

class day:
    def __init__(self, bot):
        self.bot = bot
        self.labels = labels().getLabels()

    @commands.command(pass_context=True)
    async def day(self,ctx):
        username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        if username == "":
            await ctx.bot.say("You must be registered to use this command")
            return
        dataNow = beautInfo().userStats(username)
        dataThen = database().lastStatsXP(username)
        msg = ""
        for x in range(1,24):
            info = dataNow[x].split(",")
            if int(info[2]) > dataThen[x]:
                msg += "\n`-" + self.labels[x] + ("."*(20-len(self.labels[x]))) + "{:,}".format(int(info[2]) - dataThen[x]) + "`"
        emb = embeds.Embed(title=username,description=msg, color=0xc27c0e)
        emb.set_footer(text=(ctx.message.author.nick + " " + str(datetime.date.today())), icon_url=ctx.message.author.avatar_url)
        await ctx.bot.say(embed=emb)

    
def setup(bot):
    bot.add_cog(day(bot))
    print("LOADED")