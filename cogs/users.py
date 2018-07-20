from discord.ext import commands
from discord import embeds
from lib.database import database

class users:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def users(self,ctx):
        info = database().userList(ctx.message.server.id)
        msg = ''
        for x in range(0,len(info)):
            leaderNick = await self.bot.get_user_info(info[x][1]) 
            msg +=  "`" + info[x][0] + "."*(20-len(info[x][0])) + str(leaderNick) + "`\n"
        emb = embeds.Embed(title='**Registered OSRS Accounts:**', description=msg, color=0x11806a)
        await self.bot.say(embed=emb)
        return
        
def setup(bot):
    bot.add_cog(users(bot))
    print("LOADED")