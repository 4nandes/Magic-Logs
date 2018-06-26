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
import sqlite3
import re
import datetime
import requests
from math import floor

#Create the client, open the file that has the pass in it
conn = sqlite3.connect('test.db')
c = conn.cursor()
client = discord.Client()
botSecret = open("botSecret.txt","r")
code = botSecret.read()

#Labels for all of the skills
labels = ['Overall','Attack','Defence','Strength','Hitpoints',
        'Ranged','Prayer','Magic','Cooking','Woodcutting',
        'Fletching','Fishing','Firemaking','Crafting',
        'Smithing','Mining','Herblore','Agility',
        'Thieving', 'Slayer', 'Farming','Runecrafting',
        'Hunter', 'Construction']

def searchDefault(author, server):
    c.execute("SELECT runescapeUsername FROM User WHERE discordID = {} AND serverID = {}".format(author,server))
    name = c.fetchone()
    if name:
        return name[0]
    return ""

@client.event
async def on_message(message):
    #Make sure we don't respond to ourself
    if message.author == client.user:
	    return
    #Command to compare a skill to another person
    if message.content.startswith("$flex"):
        #Gets the content after the first space which holds who we are comparing to
        skill = " ".join(message.content.split(" ")[1:2]).capitalize()
        unRec = " ".join(message.content.split(" ")[2:])
        #If they are trying to use it with a default, check for their OSRS username in the database
        unCaller = searchDefault(message.author.id,message.server.id)
        if unCaller == "":
            await client.send_message(message.channel, "You must be registered to use this command")
            return
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
        #Continues to bother the person until they input a proper skill
        proceed = False 
        while (proceed == False):
            try:
                lvlCaller = dataCaller[labels.index(skill)].split(",")
                proceed = True
            except:
                await client.send_message(message.channel, 'Could not find the skill "{}", try again'.format(skill))
                try:
                    skill = await client.wait_for_message(timeout=4.0, author=message.author)
                    skill = skill.content.capitalize()
                except:
                    await client.send_message(message.channel, "Took too long to respond")
                    return
        #Attempt to build a bar chart and a taunting message, if fail then state that the skill they input does not exist
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
        return
    #Gets the RuneScape stats for the input user and send them as a message
    elif message.content.startswith("$stats"):
        #Gets the content after the first space
        data = " ".join(message.content.split(" ")[1:])
        #If they are trying to use it with a default, check for their OSRS username in the database
        if data == "":
            data  = searchDefault(message.author.id,message.server.id)
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
        #If they are trying to use it with a default, check for their OSRS username in the database
        if data == "":
            data  = searchDefault(message.author.id,message.server.id)
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
        #If they are trying to use it with a default, check for their OSRS username in the database
        if data == "":
            data  = searchDefault(message.author.id,message.server.id)
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
            domain=dict(x=[0,0.5])
        )
        #Removing this till fixed or figured out
        trace1 = go.Bar(
            x= ["Hitpoints","Defense","Prayer"],
            y= [
                float(dataCaller[4].split(",")[1]),
                float(dataCaller[2].split(",")[1]),
                float(dataCaller[6].split(",")[1])
            ],
            text= [
                float(dataCaller[4].split(",")[1]),
                float(dataCaller[2].split(",")[1]),
                float(dataCaller[6].split(",")[1])
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
        py.image.save_as(fig, filename=(data + '.png'))
        await client.send_message(message.channel, "**" + data + "**\n`Combat Type: " + comType + "`\n`Combat Level: " + str(base) + "`")
        await client.send_file(message.channel,(data + '.png'))
        os.remove((data + '.png'))
        return
    elif message.content.startswith("$register"):
        #All of the information after the command is tried as an OSRS account
        data = " ".join(message.content.split(" ")[1:])
        try:
            sauce = urlopen("http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + data)
            soup = BeautifulSoup(sauce,'lxml')
        #If the account cannot be found then the person is told that the username does not exist
        except:
            await client.send_message(message.author, "That user does not exist")
            return
        #Checks to see if they would like to register this account name
        await client.send_message(message.channel, ("**Are you sure you would like to register the name {}**\nThis CANNOT be undone unless the admin does it manually\n('yes''Yes''y''Y')".format(data)))
        yesOrNo = await client.wait_for_message(timeout=15.0, author=message.author, channel=message.channel)
        #Uses regular expressions to see if their response starts with a Y or y
        if re.match('([y])|([Y])', yesOrNo.content):
            #Prints out 
            await client.send_message(message.channel, "Associating Discord account: **{}**\nOldSchool RuneScape account: **{}**\nCurrent Nickname: **{}**".format(message.author, data, message.author.nick))
            #Inserts them into the Database
            try:
                c.execute("INSERT INTO User VALUES(?,?,?)", (message.author.id,data,message.server.id))
                conn.commit()
                inserter = [data]
                dataCaller = soup.get_text().split("\n")
                for x in range(0,24):
                    inserter.append(dataCaller[x].split(",")[1])
                    inserter.append(dataCaller[x].split(",")[2])
                inserter.append(datetime.date.today())
                c.execute("INSERT INTO Statistic VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",inserter)
                conn.commit()
            except:
                #If they already have an account registered, then find their runescapeUsername, and tell them theyre already
                c.execute("SELECT runescapeUsername FROM User WHERE discordID = {} AND serverID = {}".format(message.author.id,message.server.id))
                name = c.fetchone()
                await client.send_message(message.channel, "**ERROR**\nThat username has already been registered with the OldSchool RuneScape account: **{}**".format(name[0]))
                return
            return
        else:
            await client.send_message(message.channel, "Aborting...")
            return
    #Prints out a list of users 
    elif message.content.startswith("$users"):
        c.execute("SELECT DISTINCT runescapeUsername, discordID FROM User WHERE serverID = {}".format(message.server.id))
        info = c.fetchall()
        msg = '**Registered OSRS Accounts:** \n'
        for x in range(0,len(info)):
            leaderNick = await client.get_user_info(info[x][1]) 
            msg +=  " \n`" + info[x][0] + "."*(20-len(info[x][0])) + str(leaderNick) + "`"
        await client.send_message(message.channel, msg)
        return
    #Gets the leaderboard for a skill of the registered users
    elif message.content.startswith("$LB"):
        data = " ".join(message.content.split(" ")[1:])
        if data == "":
            await client.send_message(message.channel, "THIS IS NOT YET IMPLEMENTED")
            return
        try:
            data = data.capitalize()
            labels.index(data)
            msg = "**{} Leaderboard:**".format(data)
            data = data.lower()
            c.execute("SELECT runescapeUsername, {}, {} FROM Statistic GROUP BY runescapeUsername ORDER BY {} DESC".format((data+'XP'),(data+'Lvl'),(data+'XP')))
            data = c.fetchall()
            for x in range(0,len(data)):
                msg += "\n`" + data[x][0] + ("."*(20-len(data[x][0])))  + "Lvl: " + str(data[x][2]) +(" "*(4-len(str(data[x][2])))) + " XP: " + "{:,}`".format(int(data[x][1]))
            await client.send_message(message.channel, msg)
            return
        except:
            await client.send_message(message.channel, "That skill was not found")
            return
    elif message.content.startswith("$GE"):
        data = " ".join(message.content.split(" ")[1:]).lower()
        try:
            sauce = requests.get("http://services.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={}".format(data)).json()
            msg = "`" + sauce['items'][0]['name']  + '`\n'
            msg += "**Price:**   " + str(sauce['items'][0]['current']['price']) + " gp"
            await client.send_message(message.channel, msg)
        except:
            await client.send_message(message.channel, "Skill not found")
            return
        return
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