from discord.ext import commands
from lib.database import database

class users:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def users(self,ctx):
        info = database().userList(ctx.message.server.id)
        msg = '**Registered OSRS Accounts:** \n'
        for x in range(0,len(info)):
            leaderNick = await ctx.bot.get_user_info(info[x][1]) 
            msg +=  " \n`" + info[x][0] + "."*(20-len(info[x][0])) + str(leaderNick) + "`"
        await ctx.bot.say(msg)
        return
        
def setup(bot):
    bot.add_cog(users(bot))
    print("LOADED")