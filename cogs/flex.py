from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels
from lib.database import database
import plotly.plotly as py
import plotly.graph_objs as go
import os


class flex:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def flex(self,ctx):
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

def setup(bot):
    bot.add_cog(flex(bot))
    print("LOADED")