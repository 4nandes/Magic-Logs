# Magic Logs ReDesign

### Reasons

- Much of the code is sloppy,  repeating, and un-maintainable
- It was thrown together as I went and is not an accurate representation of my coding habits or capabilities
- It cannot exist across multiple servers in its current state

### Goals

- Make certain it is able to function in an asynchronous manner that allows the bot to exist across many servers with no perceivable lag time between commands
- Allow the bot to use a real database rather than using a fake one like sqlite3
- Turn the bot into a presentable project that properly shows my capability as a programmer

### Steps

1. Take note of all of the commands that currently exist
2. Note all of the object types that it could create and promote more of an object oriented programming style
3. Prototype and implement a tester bot with modularity and expansion in mind
4. Design the MySQL database around this prototype so that it properly caters to the needs of the users

## Phase 1: Understand the Current Bot

### Current Commands

- **Grand Exchange**
  - Item Value Lookup
- **Member Commands**
  - Flex
  - Xp History
- **Moderator Commands**
  - Register Users
  - Check Current Roster W/Dates
  - Change Name
- **Player Lookup**
  - Combat Stats
  - Pie Chart Stats
  - Listed Stats
- **Server Lookup**
  - Leaderboard 
    - Individual Skill
    - All Skills
  - Server Roster

### Command Breakdowns (Things that I need to think about, storming process)

**Item Value Lookup:** 
	Item Object
		Constructor
		Make an embed object

**Flex Stats:**
	Character Object
		Constructor
		Comparison function
	Remove improper skill checker, make it a one off
	Drawing Object
		Bar Chart function [Character send, Character receive]
**History:**
	Function to set the compare date
	Create a character object