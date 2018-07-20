from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.database import database
from lib.labels import labels
from discord import embeds
import datetime
from datetime import timedelta

class report:
    def __init__(self, bot):
        self.bot = bot
        self.labels = labels().getLabels()
        
    # This is fine and dandy but in the end I really need to learn how decorators work
    # because this seems like a situation that is ripe for a decorator
    @commands.command(pass_context=True)
    async def report(self,ctx):
        reportLength = " ".join(ctx.message.content.split(" ")[1:]).lower()
        username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        msg = ""
        if username == "":
            await ctx.bot.say("You must be registered to use this command")
            return
        if reportLength == "":
            msg += "**{}**".format(datetime.date.today())
            dataThen = database().getStatsXP(username, datetime.date.today())
        elif reportLength == "week":
            compareDate = (datetime.date.today() - datetime.timedelta(days=7))
            msg += "**{}**".format(compareDate)
            dataThen = database().getStatsXP(username, compareDate)
        elif reportLength == "month":
            compareDate = (datetime.date.today() - datetime.timedelta(days=30))
            msg += "**{}**".format(compareDate)
            dataThen = database().getStatsXP(username, compareDate)
        elif reportLength == "all":
            dataThen = database().firstStatsXP(username)
            msg += "**{}**".format(dataThen[25])
        else:
            await self.bot.say("Accepted timeframes:\n`week/Week`\n`month/Month`\n`all/All`")
        dataNow = beautInfo().userStats(username)
        try:
            for x in range(1,24):
                info = dataNow[x].split(",")
                if int(info[2]) > dataThen[x]:
                    msg += "\n`-" + self.labels[x] + ("."*(20-len(self.labels[x]))) + "{:,}".format(int(info[2]) - dataThen[x]) + "`"
        except TypeError:
            await self.bot.say("Your account has not collected enough data to go that far back")
            return
        emb = embeds.Embed(title=username,description=msg, color=0xc27c0e)
        discordName = await ctx.bot.get_user_info(ctx.message.author.id)
        totXP = "{:,}".format(int(dataNow[0].split(",")[2]) - dataThen[0])
        emb.set_footer(text=(str(discordName) + " (" + totXP + "xp)"), icon_url=ctx.message.author.avatar_url)
        await ctx.bot.say(embed=emb)

def setup(bot):
    bot.add_cog(report(bot))
    print("LOADED")