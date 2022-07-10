# GoldyRL - Match History Bot
This is GoldyRL, a Discord bot crafted for the purpose of storing competitive match history between teams that can be later referenced by various members of a community. 

## Purposes
GoldyRL was designed with many purposes in mind:
- Community members wanting to see recent performances between teams
- Community members wanting to see previous matchups between two teams
- Casters wanting to be informed about what to expect in the coming matchup
- Graphic designers making "Recent Performances" graphics
- Broadcasters wanting to make overlays for their viewers
- Players wanting to know how other teams have performed against an upcoming opponent
- Coaches wanting to know how their team is performing against other teams

The list goes on and on with possible uses. 

## Purpose of Design
As an intern at Major League Baseball in the Summer of 2022, I realized how much data is being collected from each game and how that data proves to be useful in various ways. I saw firsthand how all of that data is being used on many different platforms. This motivated me to begin to design something similar for esports with the intention of keeping it simple and easy to use.

## Setup
When you add GoldyRL to your Discord server, please make sure that it is given the permission to write and read messages in a specific channel `match-history`. Please note this text channel must match the exact name, or GoldyRL won't be able to find it.
## Required Roles
GoldyRL's commands are designed with the intention of working with specific roles in a Discord. With it being intended for the University of Minnesota Rocket League Discord, the role structure was designed based on that. Below are the roles required:
- Captains
- Coaches
- Moderator
- Operations
## Command Permissions
GoldyRL has built-in support to determine if a member has permission to execute commands. Listed below is each command and the role that a user must have to use that command:

!commands = Everyone
!addmatch [TEAM 1] [TEAM 2] [TEAM 1 SERIES SCORE] [TEAM 2 SERIES SCORE] = Captains, Coaches, Moderator, Operations
!deletelastmatch [TEAM] = Captains, Coaches, Moderator, Operations
!reset = Operations
!getdata [TEAM] = Everyone
!getmatchupdata [TEAM] = Everyone
## Troubleshooting
__Team name has multiple words__
When you enter a team name with multiple words, wrap them in double quotes. Example: `University of Minnesota` should be entered as `"University of Minnesota"`

Any questions with setting up or getting GoldyRL to work should be directed to TitanHawk17#4522 on Discord. I'll try to respond in a timely manner.
