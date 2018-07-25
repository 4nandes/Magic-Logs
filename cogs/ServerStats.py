from discord.ext import commands
from discord import embeds
from lib.labels import labels
from lib.database import database

class ServerStats:
    def __init__(self,bot):
        self.bot = bot
        self.labels = labels().getLabels()
        self.icons = labels().getIcons()

    @commands.command(pass_context=True,aliases=['lb','leaderboard','LB'],brief='Show the leaderboard for all skills or one skill', help='Format:\n   $Leaderboard [NONE|Skill Name]')
    async def Leaderboard(self, ctx):
        data = " ".join(ctx.message.content.split(" ")[1:]).lower()
        if data == "":
            msg = database().highScores()
            emb = embeds.Embed(title="Server Leaderboard",description=msg, color=0x9b59b6)
            emb.set_thumbnail(url=self.icons[0])
            await self.bot.say(embed=emb)
            return
        try:
            msg = ""
            skillName = data.capitalize()
            data = database().leaderBoard(data)
            for x in range(0,len(data)):
                msg += "`" + data[x][0] + ("."*(20-len(data[x][0])))  + "Lvl: " + str(data[x][2]) +(" "*(4-len(str(data[x][2])))) + " XP: " + "{:,}`\n".format(int(data[x][1]))
            emb = embeds.Embed(title="{} Leaderboard:".format(skillName), description=msg, color=0x9b59b6)
            emb.set_thumbnail(url=self.icons[self.labels.index(skillName)])
            await self.bot.say(embed=emb)
            return
        except ValueError:
            await self.bot.say("That skill was not found")
            return
            
    @commands.command(pass_context=True,aliases=['users','u','U'], brief='Display the users registered to the server',help='Format:\n   $Users [NONE]')
    async def Users(self,ctx):
        info = database().userList(ctx.message.server.id)
        msg = ''
        for x in range(0,len(info)):
            leaderNick = await self.bot.get_user_info(info[x][1]) 
            msg +=  "`" + info[x][0] + "."*(20-len(info[x][0])) + str(leaderNick) + "`\n"
        emb = embeds.Embed(title='**Registered OSRS Accounts:**', description=msg, color=0x11806a)
        await self.bot.say(embed=emb)
        return

def setup(bot):
    bot.add_cog(ServerStats(bot))
    print("LOADED")