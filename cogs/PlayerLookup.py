from discord.ext import commands
from discord import embeds
from lib.beautInfo import beautInfo
from math import floor
from lib.database import database
from lib.labels import labels
import plotly.plotly as py
import plotly.graph_objs as go
import os


class PlayerLookup:
    def __init__(self,bot):
        self.bot = bot
        self.labels = labels().getLabels()
    
    @commands.command(pass_context=True,aliases=['combat','c','C'], brief='Display combat statistics', help='Format:\n   $Combat [NONE|OSRS Account Name]')
    async def Combat(self, ctx):
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            self.bot.say("That username was not found")
            return
        base = .25*(float(data[2].split(",")[1]) + float(data[4].split(",")[1]) + floor(float(data[6].split(",")[1])/2))
        melee = .325*(float(data[1].split(",")[1]) + float(data[3].split(",")[1]))
        ranged = .325*(floor(float(data[5].split(",")[1])/2) + float(data[5].split(",")[1]))
        mage = .325*(floor(float(data[7].split(",")[1])/2) + float(data[7].split(",")[1])) 
        comType = ["", ""]
        if melee > ranged and melee > mage:
            comType[0] = "Warrior"
            comType[1] = 'https://vignette.wikia.nocookie.net/2007scape/images/f/fe/Attack_icon.png/revision/latest?cb=20180424002328'
            base = base + melee
        elif mage > ranged:
                comType[0] = "Mage"
                comType[1] = 'https://vignette.wikia.nocookie.net/2007scape/images/5/5c/Magic_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010803'
                base = base + mage
        else:
            comType[0] = "Ranger"
            comType[1] = 'https://vignette.wikia.nocookie.net/2007scape/images/1/19/Ranged_icon.png/revision/latest/scale-to-width-down/21?cb=20180424010745'
            base = base + ranged
        #Traces out the pie chart for combat breakdown
        trace = go.Pie(
            labels=["Attack + Strength","Ranged","Magic"], 
            values=[melee,ranged,mage], 
            textinfo="label", 
            showlegend=False,
            marker=dict(line=dict(color='#000000', width=1.5)),
            textposition="inside",
            domain=dict(x=[0,0.5])
        )
        #Removing this till fixed or figured out
        trace1 = go.Bar(
            x= ["Hitpoints","Defense","Prayer"],
            y= [
                float(data[4].split(",")[1]),
                float(data[2].split(",")[1]),
                float(data[6].split(",")[1])
            ],
            text= [
                float(data[4].split(",")[1]),
                float(data[2].split(",")[1]),
                float(data[6].split(",")[1])
            ],
            textposition = 'auto',
            showlegend=False,
            marker=dict(color=['#8b0000','#808080',"#ffff00"])
        )
        #Sets the layout for the charts
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            width=2000, 
            height=1000, 
            font=dict(
                family='sans serif', 
                size=50, 
                color='#000000'
            ),
            xaxis=dict(domain=[0.55,1])
        )
        #Creates the figure, saves that figure as an image, submits the image along with a message about the character then returns
        fig = go.Figure(data=[trace,trace1], layout=layout)
        py.image.save_as(fig, filename=(username + '.png'))
        await self.bot.say("**" + username + "**\n`Combat Type: " + comType[0] + "`\n`Combat Level: " + str(base) + "`")
        await self.bot.upload(username + '.png')
        os.remove(username + '.png')
        return
    
    @commands.command(pass_context=True,aliases=['p','pie'],brief='Display an XP pie chart', help='Format:\n   $Pie [NONE|OSRS Account Name]')
    async def Pie(self,ctx):
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

    @commands.command(pass_context=True,aliases=['s','S','stats'], brief='Displays account statistics', help='Format:\n   $Stats [NONE|OSRS Account Name]')
    async def Stats(self, ctx):
        username = " ".join(ctx.message.content.split(" ")[1:])
        if username == "":
            username = database().searchDefault(ctx.message.author.id,ctx.message.server.id)
        data = beautInfo().userStats(username)
        if data == "":
            await self.bot.say("That username could not be found")
            return
        title = "**" + username + "'s stats:**"
        msg = ''
        for x in range(0,24):
            info = data[x].split(",")
            msg += "`-" + self.labels[x] + ("."*(20-len(self.labels[x]))) + "Lvl: " + info[1] +(" "*(4-len(info[1]))) + " XP: " + "{:,}".format(int(info[2])) + "`\n"
        emb = embeds.Embed(title=title,description=msg, color=0x206694)
        await self.bot.say(embed=emb)
        return
def setup(bot):
    bot.add_cog(PlayerLookup(bot))
    print("LOADED")