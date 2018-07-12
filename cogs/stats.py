from discord.ext import commands
from discord import embeds
from lib.beautInfo import beautInfo
from lib.labels import labels
from lib.database import database

class stats:
    """
    This is the class for the command $stats for flexBot on discord
    """
    def __init__(self, bot):
        self.bot = bot
        self.labels = labels().getLabels()
    
    @commands.command(pass_context=True)
    async def stats(self, ctx):
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            await ctx.bot.say("That username could not be found")
            return
        title = "**" + username + "'s stats:**"
        msg = ''
        for x in range(0,24):
            info = data[x].split(",")
            msg += "`-" + self.labels[x] + ("."*(20-len(self.labels[x]))) + "Lvl: " + info[1] +(" "*(4-len(info[1]))) + " XP: " + "{:,}".format(int(info[2])) + "`\n"
        emb = embeds.Embed(title=title,description=msg, color=0x206694)
        await ctx.bot.say(embed=emb)
        return

def setup(bot):
    bot.add_cog(stats(bot))
    print("LOADED")