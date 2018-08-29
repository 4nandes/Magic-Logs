![MagicLogs](https://vignette.wikia.nocookie.net/2007scape/images/a/ac/Magic_logs_detail_animated.gif/revision/latest?cb=20180205042632) 
#Magic Logs 
**Magic Logs** is a python script that runs a Discord bot. Discord is a chat service that keeps conversations that have many users organized. The general purpose of the bot is to retrieve, display, and track Old School Runescape account statistics within Discord.  

It all started as a joke, a small script that a friend and I used to tell each other how much more XP we had in a particular skill (Flex command). Over time more commands were added to the bot, and now the bot has its own Discord community that has built up around it. 

The name of the chat bot is inspired by the name of an in-game item "Magic Logs", because the bot behaves like a "magical" set of logged character data. 

If you would like to join the Dicord:
![Invite Link](https://discord.gg/DZqKTun) *

*_Please note that this invite link is set up such that if you do not get a role assigned to you upon entering the server, you will be automatically kicked from it once you log out._

## Commands:
### $GE
Format: `$GE [Item Name]`

Looks up the given item and returns its:
- Current Price
- Change in value in the last 24 hours
- Percent change in the last 30 days
- High alchemy profit
- Flavor Text
- Icon

![GE](https://i.imgur.com/Z2nIzdY.png)
### $Flex
Format: `$flex [Skill Name] [OSRS Username]`

This command is only available to those who have a registered account.

To use this command, put the account you would like to compare your account to in the OSRS Username field. The bot will then direct message you and ask what skill you would like to compare. After you have provided a proper skill, it will submit the amount of difference between your account and the account provided with a bar graph.

![flex](https://i.imgur.com/PIJegbt.png)
### $History
Format: `$history [NONE|week|month|all]`

This command is only available to those who have a registered account.

This command will display the amount of XP that you have gained since the last XP snaphot (currently taken at 4AM PST) if you do not put anything after the command. Effectively this shows you the amount of XP that you have gained in the last 24 hours. If the bot has been tracking you for long enough, then you can use the week, month, or all option to show the amount of XP gained in the last week, month or since you started tracking your stats.

![History](https://i.imgur.com/5r07Ayz.png)
### $Register
Format: `$Register @[Discord User]`

You must have a "Mod" role to use this command

Registers a Runescape username to a Discord account. A mod may use this command on a Discord user to register their account to that particular discord server. Once you invoke the command, the bot will ask what OSRS username you would like to register to that account. If done properly, it should enable the ability to use the $flex command as well as using defaults on the $stats, $pie and $combat commands. The bot will walk you through the registration process, and will tell you when it has completed properly.

![register](https://i.imgur.com/af2qu2V.png)
### $Pie
Format: `$Pie [OSRS Username]`

If the `[OSRS Username]` is left blank and your account is registered, then the command will use your registered username

Gets and displays the statistics for an OSRS username in pie chart form. It seperates the pie based on XP. If the username's statistics cannot be found then the bot will notify the user of this.

![pie](https://i.imgur.com/l7o63EX.png)
### $Stats
Format: `$Stats [OSRS Username]`

If the `[OSRS Username]` is left blank and your account is registered, then the command will use your registered username

Gets and displays the statistics for the OSRS username that was provided, if the username's statistics cannot be found then the bot will notify the user of this.

![stats](https://i.imgur.com/III0bA2.png)
### $Combat
Format: `$Combat [OSRS Username]`

If the `[OSRS Username]` is left blank and your account is registered, then the command will use your registered username

Gets and displays the combat statistics for is OSRS username that was provided. If the username's statistics cannot be found then the bot will notify the user of this. The bot also displays the breakdown of how their combat lvl is calculated.

![combat](https://i.imgur.com/XeK42r8.png)
### $Users
Format: `$Users`

Gets and displays the OSRS usernames that have been registered to the server so far.

![users](https://i.imgur.com/g0E4ngq.png)
### $Leaderboard
Format: `$Leaderboard [Skill Name]`

Gets and displays the leaderboard for the skill provided, if the skill cannot be found then the user will be notified with a DM that that skill could not be found. 

If the `[Skill Name]` is left blank then the leaderboard of all skills is displayed along with the name of the person with the highest amount of XP in that skill.

![LB](https://i.imgur.com/ubyDEp7.png)
## Sources:
### discord.py
https://github.com/Rapptz/discord.py

This is a wonderful tool that was made by "Danny" Rapptz. It allows for the communication between a bot and Discord.
### Plotly
https://plot.ly/python/

Plotly is a python library that allows the bot to make visually pleasing graphs
### Beautiful Soup
https://www.crummy.com/software/BeautifulSoup/

Beautiful Soup is a python library that allows the bot to get information off of the OSRS hiscore website.

## Future Plans:
- Weekly gain leaderboard posted every sunday
- Website for the bot
- Ability to add roles by reacting to the bot with an emoji (Discord Feature)
