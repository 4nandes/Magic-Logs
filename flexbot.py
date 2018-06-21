#░░░░░░░░▄▄▄▀▀▀▄▄███▄░░░░░░░░░░░░░░
#░░░░░▄▀▀░░░░░░░▐░▀██▌░░░░░░░░░░░░░
#░░░▄▀░░░░▄▄███░▌▀▀░▀█░░░░░░░░░░░░░
#░░▄█░░▄▀▀▒▒▒▒▒▄▐░░░░█▌░░░░░░░░░░░░
#░▐█▀▄▀▄▄▄▄▀▀▀▀▌░░░░░▐█▄░░░░░░░░░░░
#░▌▄▄▀▀░░░░░░░░▌░░░░▄███████▄░░░░░░
#░░░░░░░░░░░░▐░░░░▐███████████▄░░░
#░░Author:░░░░▐░░░░▐█████████████▄
#░░░Nathan░░░░░▀▄░░░▐█████████████▄
#░░░░░Fernandes░░░▀▄▄███████████████
#░░░░░░░░░░░░░░░░░░░░░░░░█▀██████░░
import discord
from bs4 import BeautifulSoup
from urllib.request import urlopen
import plotly.plotly as py
import plotly.graph_objs as go
import os
from math import floor

#Create the client, open the file that has the pass in it
client = discord.Client()
botSecret = open("botSecret.txt","r")
code = botSecret.read()

#Having these is embarassing, theyre most likely unneccessary, and also its repeating information
#skillNames = {0:'Overall', 1:'Attack', 2:'Defence', 
#            3:'Strength', 4:'Hitpoints', 5:'Ranged', 
#            6:'Prayer', 7:'Magic', 8:'Cooking', 
#            9:'Woodcutting', 10:'Fletching', 11:'Fishing', 
#            12:'Firemaking', 13:'Crafting', 14:'Smithing', 
#            15:'Mining', 16:'Herblore', 17:'Agility', 
#            18:'Thieving', 19:'Slayer', 20:'Farming', 
#            21:'Runecrafting', 22:'Hunter', 23:'Construction'}
#book = {'overall':0, 'attack':1, 'defence':2, 
#        'strength':3, 'hitpoints':4, 'ranged':5, 
#        'prayer':6, 'magic':7, 'cooking':8, 
#        'woodcutting':9, 'fletching':10, 'fishing':11, 
#        'firemaking':12, 'crafting':13, 'smithing':14, 
#        'mining':15, 'herblore':16, 'agility':17, 
#        'thieving':18, 'slayer':19, 'farming':20, 
#        'runecrafting':21, 'hunter':22, 'construction':23}
labels = ['Overall','Attack','Defence','Strength','Hitpoints',
        'Ranged','Prayer','Magic','Cooking','Woodcutting',
        'Fletching','Fishing','Firemaking','Crafting',
        'Smithing','Mining','Herblore','Agility',
        'Theiving', 'Slayer', 'Farming','Runecrafting',
        'Hunter', 'Construction']

@client.event
async def on_message(message):
    #Make sure we don't respond to ourself
    if message.author == client.user:
	    return
    #Command to compare a skill to another person
    if message.content.startswith("$flex"):
        #Collect the names of the two accounts to compare
        await client.send_message(message.author, "Enter the name of your account: ")
        unCaller = await client.wait_for_message(timeout=15.0, author=message.author)
        unCaller = unCaller.content
        await client.send_message(message.author, "Enter the name of the account that we are flexing on today: ")
        unRec = await client.wait_for_message(timeout=15.0, author=message.author)
        unRec = unRec.content
        #Attempt to get both of their data from the OSRS highscores website, if either throws an error, then
        #we will send a message stating that one of the two usernames that was submitted was improper
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + unCaller)
            soup = BeautifulSoup(sauce,'lxml')
            dataCaller = soup.get_text().split("\n")
            ranch = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player="  + unRec)
            stew = BeautifulSoup(ranch,'lxml')
            dataRec = stew.get_text().split("\n")
        except:
            await client.send_message(message.author, "One or both of the usernames provided does not have public highscore data")
            return
        #Propmt user for the type of skill that they want to compare
        await client.send_message(message.author, "What skill are you comparing?")
        skill = await client.wait_for_message(timeout=15.0, author=message.author)
        skill = skill.content.capitalize()
        #Attempt to build a bar chart and a taunting message, if fail then state that the skill they input does not exist
        try:
            lvlCaller = dataCaller[labels.index(skill)].split(",") 
            lvlRec = dataRec[labels.index(skill)].split(",")
            if int(lvlCaller[1]) > int(lvlRec[1]):
                await client.send_message(message.channel, 
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
                await client.send_file(message.channel,(unCaller + '.png'))
                await client.send_message(message.channel, "*Sit kid*")
                os.remove((unCaller + '.png'))
        except:
            await client.send_message(message.author, "That skill does not exist")
            return
        return
    #Gets the RuneScape stats for the input user and send them as a message
    elif message.content.startswith("$stats"):
        #Gets the content after the first space
        data = " ".join(message.content.split(" ")[1:])
        #Gets the data for that account from the OSRS highscore website, if errors occur it messages that
        #that user does not exist
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + data)
            soup = BeautifulSoup(sauce,'lxml')
        except:
            await client.send_message(message.author, "That user does not exist")
            return
        #Split the data by newline, as it comes in in sets of three values per line comma separated
        dataCaller = soup.get_text().split("\n")
        #Print out in bold the character name, then for loop through all of the skills.
        #Adds the lines to string variable named "msg" that starts out empty
        msg = "**" + data + "'s stats:**\n"
        for x in range(0,24):
            info = dataCaller[x].split(",")
            msg += "`-" + labels[x] + ("."*(20-len(labels[x]))) + "Lvl: " + info[1] +(" "*(4-len(info[1]))) + " XP: " + "{:,}".format(int(info[2])) + "`\n"
        await client.send_message(message.channel, msg)
        return
    #Get the stats on an account, and display a pie chart with the breakdown of those stats
    elif message.content.startswith("$pie"):
        #Creates a list named "levels" that will store the values for the pie chart, gets the name of the chart to pie
        levels = []
        data = " ".join(message.content.split(" ")[1:])
        #Attempts to get the information on the character that was submitted, if error then sends error message to user
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + data)
            soup = BeautifulSoup(sauce,'lxml')
        except:
            await client.send_message(message.author, "That user does not exist")
            return
        #Splits the data that we took in by newlines, and then goes through it and appends the XP collumn to levels
        dataCaller = soup.get_text().split("\n")
        for x in range(1,24):
            levels.append(int(dataCaller[x].split(",")[2]))
        #Creates the pie chart with the previously appended data
        trace = go.Pie(
            labels=labels[1:], 
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
        py.image.save_as(fig, filename=(data + '.png'))
        await client.send_message(message.channel,("**" + data + "'s XP breakdown:**\n" ))
        await client.send_file(message.channel,(data + '.png'))
        os.remove((data + '.png'))
        return
    #Get the combat level of an account and display the reason that the level is that way
    elif message.content.startswith("$combat"):
        #Gets the values after the command and saves it in data
        data = " ".join(message.content.split(" ")[1:])
        #Tries to get the score for the submitted character, if error sends error message to discord
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + data)
            soup = BeautifulSoup(sauce,'lxml')
        except:
            await client.send_message(message.author, "That user does not exist")
            return
        #Separates the data by newline. Sets the base, melee, ranged, and mage values
        dataCaller = soup.get_text().split("\n")
        base = .25*(float(dataCaller[2].split(",")[1]) + float(dataCaller[4].split(",")[1]) + floor(float(dataCaller[6].split(",")[1])/2))
        melee = .325*(float(dataCaller[1].split(",")[1]) + float(dataCaller[3].split(",")[1]))
        ranged = .325*(floor(float(dataCaller[5].split(",")[1])/2) + float(dataCaller[5].split(",")[1]))
        mage = .325*(floor(float(dataCaller[7].split(",")[1])/2) + float(dataCaller[7].split(",")[1]))
        #Create an empty string and then set it to the largest of the three types of combat 
        comType = ""
        if melee > ranged and melee > mage:
            comType = "Warrior"
            base = base + melee
        elif mage > ranged:
                comType = "Mage"
                base = base + mage
        else:
            comType = "Ranger"
            base = base + ranged
        #Traces out the pie chart for combat breakdown
        trace = go.Pie(
            labels=["Attack + Strength","Ranged","Magic"], 
            values=[melee,ranged,mage], 
            textinfo="label", 
            showlegend=False,
            marker=dict(line=dict(color='#000000', width=1.5)),
            textposition="inside",
            domain=dict(x=[0,4])
        )
        #Removing this till fixed or figured out
        #trace1 = go.Bar(
        #    x= ["Hitpoints","Defense","Prayer"],
        #    y= [
        #        float(dataCaller[4].split(",")[1]),
        #        float(dataCaller[2].split(",")[1]),
        #        float(dataCaller[6].split(",")[1])
        #    ],
        #    textposition = 'auto',
        #    showlegend=False,
        #    marker=dict(color=['#8b0000','#8b0000',"#8b0000"])
        #)
        #Sets the layout for the charts
        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            width=1000, 
            height=1000, 
            font=dict(
                family='sans serif', 
                size=40, 
                color='#000000'
            ) 
        )
        #Creates the figure, saves that figure as an image, submits the image along with a message about the character then returns
        fig = go.Figure(data=[trace], layout=layout)
        py.image.save_as(fig, filename=(data + '.png'))
        await client.send_message(message.channel, "**SLIGHTLY BROKEN COMMAND STILL \n" + data + "**\n`Combat Type: " + comType + "`\n`Combat Level: " + str(base) + "`")
        await client.send_file(message.channel,(data + '.png'))
        os.remove((data + '.png'))
        return

#Once the bot is logged in, print this out to the console so that I know its in             
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    await client.change_presence(game=discord.Game(name="you sleep", type=3))
    print(client.user.id)
    print('------')

#Starts up the client with the key that was retrieved from botSecret
client.run(code)