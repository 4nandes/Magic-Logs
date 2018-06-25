# FlexBot
FlexBot is a python script that runs a Discord bot. The general purpose of the bot is to retrieve and display OSRS character data. Its inspiration is from the really stale meme [detailed here.][stale]

[stale]:http://knowyourmeme.com/memes/u-ever-flex-on-niggas
## Commands:
### $stats
Format: `$stats [OSRS Username]`

Gets and displays the statistics for the OSRS username that was provided, if the username's statistics cannot be found then the bot will notify the user of this.

![stats](https://i.imgur.com/WxwJOrx.png)
### $pie
Format: `$pie [OSRS Username]`

Gets and displays the statistics for an OSRS username in pie chart form. It seperates the pie based on XP. If the username's statistics cannot be found then the bot will notify the user of this.

![pie](https://i.imgur.com/pUfDwct.png)
### $flex
Format: `$flex [OSRS Username]`

THIS COMMAND HAS CHANGED, UPDATED MARKDOWN COMING SOON

The most complicated of the commands that the bot currently has. After this command has been recieved the bot will direct message the user asking for an account to compare to, and then a skill to compare. If either of the provided accounts cannot be found or if the provided skill does not exist then the bot will notify the user of this. If all of the provided input is correct then the bot will display a comparison of the submitted skill using a bar graph in chat.

![flex](https://i.imgur.com/Q4hgEcI.png)
### $combat
Format: `$combat [OSRS Username]`

This skill is still under construction, I need to find out how to get subplots to work side by side.

Gets and displays the combat statistics for is OSRS username that was provided. If the username's statistics cannot be found then the bot will notify the user of this. The bot also displays the breakdown of how their combat lvl is calculated.

![combat](https://i.imgur.com/0P69m20.png)
## Sources:
### discord.py
https://github.com/Rapptz/discord.py

This is a wonderful tool that was made by "Danny" Rapptz. It allows for the communication between a bot and Discord.
### Plotly
https://plot.ly/python/

Plotly is a python library that allows the bot to make visually pleasing graph images
### Beautiful Soup
https://www.crummy.com/software/BeautifulSoup/

Beautiful Soup is a python library that allows the bot to get information off of the OSRS hiscore website.

## Future Plans:
- Grand exchange search function
- Daily gain leaderboard automation on Monday - Saturday, Weekly gain leaderboard Sunday
- Fixing the $combat command
- Website for the bot
- WhoIs/WhoAmI commands

6/25/18 (Need to update with $LB and register stuff, and changes to $flex)