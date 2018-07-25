from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels
from lib.database import database
from discord import embeds
import datetime as dt
from datetime import datetime, timedelta, date, time
import plotly.plotly as py
import plotly.graph_objs as go
import re
import os

class MemberCommands:
    def __init__(self, bot):
        self.bot = bot
        self.labels = labels().getLabels()
    @commands.command(pass_context=True,aliases=['flex','f','F'],brief='Compare your XP in a skill with another account',help='Format:\n   $Flex [Skill Name] [Account to compare to]')
    async def Flex(self,ctx):
        #Gets the content after the first space which holds who we are comparing to
        skill = " ".join(ctx.message.content.split(" ")[1:2]).capitalize()
        unRec = " ".join(ctx.message.content.split(" ")[2:])
        #If they are trying to use it with a default, check for their OSRS username in the database
        unCaller = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        if unCaller == "":
            await self.bot.say("You must be registered to use this command")
            return
        #Attempt to get both of their data from the OSRS highscores website, if either throws an error, then
        #we will send a message stating that one of the two usernames that was submitted was improper
        
        dataCaller = beautInfo().userStats(unCaller)
        dataRec = beautInfo().userStats(unRec)
        if dataRec == "":
            await self.bot.say("One or both of the usernames provided does not have public highscore data") 
            return
        #Continues to bother the person until they input a proper skill
        proceed = False 
        while (proceed == False):
            try:
                lvlCaller = dataCaller[labels().index(skill)].split(",")
                proceed = True
            except ValueError:
                await self.bot.say('Could not find the skill "{}", try again'.format(skill))
                try:
                        skill = await self.bot.wait_for_message(timeout=4.0, author=ctx.message.author)
                        skill = skill.content.capitalize()
                except AttributeError:
                        await self.bot.say("Took too long to respond")
                        return
        #Attempt to build a bar chart and a taunting message, if fail then state that the skill they input does not exist
        lvlCaller = dataCaller[labels().index(skill)].split(",") 
        lvlRec = dataRec[labels().index(skill)].split(",")
        if int(lvlCaller[1]) > int(lvlRec[1]):
            await self.bot.say( 
            "You ever show off your lvl.%d in %s just to flex on them %s niggas?\n**Flex Strength:** %d Levels %s XP" 
            %(int(lvlCaller[1]),skill,unRec,(int(lvlCaller[1]) - int(lvlRec[1])),"{:,}".format((int(lvlCaller[2]) - int(lvlRec[2])))))
            #Traces out the bar chart
            trace1 = go.Bar(
                x= [unCaller, unRec],
                y= [int(lvlCaller[2]),int(lvlRec[2])],
                text= ["{:,}".format(int(lvlCaller[2])),"{:,}".format(int(lvlRec[2]))],
                textposition = 'auto',
                marker=dict(color=['#16a085','#cb4335'])
            )
            #Layout for the bar chart
            layout = go.Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='sans serif', size=26, color='#ffffff')
            )
            #Create the chart, save as image, submit image, delete image
            fig = go.Figure(data=[trace1], layout=layout)
            py.image.save_as(fig, filename=(unCaller + '.png'))
            await self.bot.upload(unCaller + '.png')
            await self.bot.say("*Sit kid*")
            os.remove((unCaller + '.png'))
        return
        
    # This is fine and dandy but in the end I really need to learn how decorators work
    # because this seems like a situation that is ripe for a decorator
    @commands.command(pass_context=True, aliases=['history','H','h'], brief='Shows the XP gained in a day, week, or month', help='Format:\n   $History [NONE|week|month|all]')
    async def History(self,ctx):
        reportLength = " ".join(ctx.message.content.split(" ")[1:]).lower()
        username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        msg = ""
        if username == "":
            await self.bot.say("You must be registered to use this command")
            return
        if reportLength == "":
            msg += "**{}**".format(date.today())
            now = datetime.now()
            day = date.today()
            if time(0,00) <= now.time() <= time(4,00):
                day = (day - dt.timedelta(days=1))
            dataThen = database().getStatsXP(username, day)
        elif reportLength == "week":
            compareDate = (date.today() - dt.timedelta(days=7))
            msg += "**{}**".format(compareDate)
            dataThen = database().getStatsXP(username, compareDate)
        elif reportLength == "month":
            compareDate = (date.today() - dt.timedelta(days=30))
            msg += "**{}**".format(compareDate)
            dataThen = database().getStatsXP(username, compareDate)
        elif reportLength == "all":
            dataThen = database().firstStatsXP(username)
            msg += "**{}**".format(dataThen[24])
        else:
            await self.bot.say("Accepted timeframes:\n`week`\n`month`\n`all`")
            return
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
        discordName = await self.bot.get_user_info(ctx.message.author.id)
        totXP = "{:,}".format(int(dataNow[0].split(",")[2]) - dataThen[0])
        emb.set_footer(text=(str(discordName) + " (" + totXP + "xp)"), icon_url=ctx.message.author.avatar_url)
        await self.bot.say(embed=emb)
        return
        
    @commands.command(pass_context=True,aliases=['register'], brief='Register your OSRS account to this server', help='Format:\n   $Register [OSRS Account Name]')
    async def Register(self,ctx):
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            await self.bot.say("That username could not be found")
            return
        #Checks to see if they would like to register this account name
        await self.bot.say("**Are you sure you would like to register the name {}**\nThis CANNOT be undone unless the admin does it manually\n('yes''Yes''y''Y')".format(username))
        yesOrNo = await self.bot.wait_for_message(timeout=15.0, author=ctx.message.author, channel=ctx.message.channel)
        #Uses regular expressions to see if their response starts with a Y or y
        if re.match('([y])|([Y])', yesOrNo.content):
            #Prints out 
            await self.bot.say("Associating Discord account: **{}**\nOldSchool RuneScape account: **{}**\nCurrent Nickname: **{}**".format(ctx.message.author, username, ctx.message.author.nick))
            #Inserts them into the Database
            if not database().newUser(ctx.message.author.id,username,ctx.message.server.id):
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

def setup(bot):
    bot.add_cog(MemberCommands(bot))
    print("LOADED")