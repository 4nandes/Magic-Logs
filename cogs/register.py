from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels
from lib.database import database
import re
import datetime

class register:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def register(self,ctx):
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            await ctx.bot.say("That username could not be found")
            return
        #Checks to see if they would like to register this account name
        await ctx.bot.say("**Are you sure you would like to register the name {}**\nThis CANNOT be undone unless the admin does it manually\n('yes''Yes''y''Y')".format(username))
        yesOrNo = await ctx.bot.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
        #Uses regular expressions to see if their response starts with a Y or y
        if re.match('([y])|([Y])', yesOrNo.content):
            #Prints out 
            await ctx.bot.say("Associating Discord account: **{}**\nOldSchool RuneScape account: **{}**\nCurrent Nickname: **{}**".format(ctx.message.author, username, ctx.message.author.nick))
            #Inserts them into the Database
            if not database().newUser(ctx.message.author.id,username,ctx.message.server.id):
                await ctx.bot.say("Something went wrong with registering your DiscordID to this server, contact dev")
                return
            inserter = [username]
            for x in range(0,24):
                inserter.append(data[x].split(",")[1])
                inserter.append(data[x].split(",")[2])
            inserter.append(datetime.date.today())
            if not database().insertStats(inserter):
                name = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
                await ctx.bot.say("That username has been registered with the OldSchool RuneScape account: **{}** in another server\nIf this was your doing, great. If it is not, contact dev.".format(name))
                return
            return
        else:
            await ctx.bot.say("Aborting...")
            return


def setup(bot):
    bot.add_cog(register(bot))
    print("LOADED")