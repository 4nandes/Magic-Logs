from discord.ext import commands
from discord import utils
from lib.beautInfo import beautInfo
from lib.database import database
import datetime as dt
import re

class ModCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,aliases=['register'], brief='Register your OSRS account to this server', help='Format:\n   $Register [OSRS Account Name]')
    async def Register(self,ctx):
        isMod = utils.get(ctx.message.author.roles, name="Mod")
        if isMod:
            discMention = " ".join(ctx.message.content.split(" ")[1:])
            await self.bot.say('Register ' + discMention + '?')
            yesOrNo = await self.bot.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
            if re.match('([y])|([Y])', yesOrNo.content):
                await self.bot.say("What is the name of the OSRS account that we are registering to " + discMention + "?")
                username = await self.bot.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
                username = username.content
                print(username)
                data = beautInfo().userStats(username)
                if data == "":
                    await self.bot.say("That username could not be found")
                    return
                #Checks to see if they would like to register this account name
                await self.bot.say("**Are you sure you would like to register the name {}**\n('yes''Yes''y''Y')".format(username))
                yesOrNo = await self.bot.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
                #Uses regular expressions to see if their response starts with a Y or y
                if re.match('([y])|([Y])', yesOrNo.content):
                    #Prints out
                    discName = await self.bot.get_user_info(discMention[2:-1]) 
                    await self.bot.say("Associating Discord account: **{}**\nOldSchool RuneScape account: **{}**\n".format(discName, username))
                    #Inserts them into the Database
                    if not database().newUser(discMention[2:-1],username,ctx.message.server.id):
                        await self.bot.say("Something went wrong with registering your DiscordID to this server, contact dev")
                        return
                    inserter = [username]
                    for x in range(0,24):
                        inserter.append(data[x].split(",")[1])
                        inserter.append(data[x].split(",")[2])
                    inserter.append(dt.date.today())
                    if not database().insertStats(inserter):
                        name = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
                        await self.bot.say("That username has been registered with the OldSchool RuneScape account: **{}** in another server\nIf this was your doing, great. If it is not, contact dev.".format(name))
                        return
                    return
                else:
                    await self.bot.say("Aborting...")
                    return
            else:
                await self.bot.say("Aborting...")
                return
        else:
            await self.bot.say("This is a Moderator only commmand")
            return

def setup(bot):
    bot.add_cog(ModCommands(bot))
    print("LOADED")