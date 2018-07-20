from discord.ext import commands
from lib.beautInfo import beautInfo
from lib.labels import labels
from lib.database import database
import plotly.plotly as py
import plotly.graph_objs as go
import os

class pie:
    """
    This is the class for the command $pie for flexBot on discord
    """
    def __init__(self,bot):
        self.bot = bot
        self.labels = labels().getLabels()
    
    @commands.command(pass_context=True)
    async def pie(self,ctx):
        levels = []
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            await self.bot.say("That username does not exist")
            return
        for x in range(1,24):
            levels.append(int(data[x].split(",")[2]))
        trace = go.Pie(
            labels=self.labels[1:], 
            values=levels, 
            textinfo="label", 
            showlegend=False,
            marker=dict(
                line=dict(
                    color='#000000', 
                    width=1.5
                )
            ),
            textposition="inside"
        )
        #Sets the layout for the Pie chart, things like a clear background, outlines, font, etc.
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            width=1000, height=1000, 
            font=dict(
                family='sans serif', 
                size=26, 
                color='#000000'
            )
        )
        #Creates the figure with the data and the layou and then saves the file in the same name as the character 
        #that is being checked. It then submits that picture along with the proper message.
        #Finally it deletes the picture and returns
        fig = go.Figure(data=[trace], layout=layout)
        py.image.save_as(fig, filename=(username + '.png'))
        await self.bot.say("**" + username + "'s XP breakdown:**\n" )
        await self.bot.upload(username + '.png')
        os.remove((username + '.png'))

def setup(bot):
    bot.add_cog(pie(bot))
    print("LOADED")