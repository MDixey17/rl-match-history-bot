import discord
from discord.ext import commands
import sqlite3
from datetime import date

bot = commands.Bot(command_prefix="!")
red_color = int(0x7A0019)

conn = sqlite3.connect("match_results.db")
cur = conn.cursor()

insert_query = """INSERT INTO match_history VALUES (?,?,?,?,?);"""

def get_help_embed():
    embed = discord.Embed(title='GoldyRL Accepted Commands', color=red_color)
    embed.add_field(name="!commands", value="Prints this message", inline=False)
    embed.add_field(name="!addmatch [UMN TEAM] [OPPONENT] [UMN SERIES SCORE] [OPPONENT SERIES SCORE]", value="Add a completed match.\n", inline=False)
    embed.add_field(name="!deletelastmatch [UMN TEAM]", value="Delete the last match for a UMN Team.\n", inline=False)
    embed.add_field(name="!reset", value="Delete all matchup data.\n", inline=False)
    embed.add_field(name="!getdata [TEAM]", value="Retrieve all data for TEAM.\n", inline=False)
    embed.add_field(name="!getmatchupdata [UMN TEAM] [OPPONENT TEAM]", value="Retrieve all data between UMN and Opponent.\n", inline=False)
    return (embed)

def get_start_embed():
    return (discord.Embed(title='GoldyRL', description="Hey there! I'm GoldyRL, the Discord bot designed to store all UMN Esports matches in the last three months. If you don't know how to use me, type !commands in this channel. Otherwise, type away.", color=red_color))

def get_success_embed(cmd):
    embed = discord.Embed(title='GoldyRL - Successful Command', description="Command was successfully executed and the database has been updated!\n", color=red_color)
    embed.add_field(name="Command", value=cmd, inline=False)
    return (embed)

def get_fail_embed(cmd):
    embed = discord.Embed(title='GoldyRL - Failed Command', description="Command failed to execute!\n", color=red_color)
    embed.add_field(name="Command", value=cmd, inline=False)
    return (embed)

def get_results_embed():
    embed = discord.Embed(title="GoldyRL - Retrieved Data", description="I found some data that you requested!\n", color=red_color)
    return (embed)

def get_reset_embed():
    embed = discord.Embed(title="GoldyRL - Data Reset", description="All match results data has been deleted and reset!\n", color=red_color)
    return (embed)

def get_nodata_embed():
    embed = discord.Embed(title="GoldyRL - No Data Found", description="I wasn't able to find any data with those arguments!\n", color=red_color)
    return (embed)

def get_nopermission_embed():
    embed = discord.Embed(title="GoldyRL - Invalid Permissions", description="Sorry, but you don't have the permissions to execute that command!\n", color=red_color)
    return (embed)

@bot.event
async def on_ready():
    cur.execute("""
        SELECT count(name) FROM sqlite_master WHERE type='table' AND name='match_history'
    """)
    if cur.fetchone()[0]==1 : 
        print('match_history table exists.')

    else :
        print('Table does not exist. Making match_history table')
        cur.execute("""
            CREATE TABLE match_history (
                team_one text,
                team_two text,
                team_one_score integer,
                team_two_score integer,
                date text
            )
        """)
        conn.commit()

    match_history_channel = discord.utils.get(bot.get_all_channels(), name='match-history')
    await match_history_channel.send(embed=get_start_embed())
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
# ROLES = everyone
async def commands(ctx):
    await ctx.send(embed=get_help_embed())

@bot.command()
# ROLES = Captain, Coach, Moderator, Operations
async def addmatch(ctx, team1, team2, team1_score: int, team2_score: int):
    captain_role = discord.utils.get(ctx.guild.roles, name="Captains")
    coach_role = discord.utils.get(ctx.guild.roles, name="Coaches")
    moderator_role = discord.utils.get(ctx.guild.roles, name="Moderator")
    ops_role = discord.utils.get(ctx.guild.roles, name="Operations")
    if (captain_role in ctx.author.roles or coach_role in ctx.author.roles or moderator_role in ctx.author.roles or ops_role in ctx.author.roles):
        today = date.today().strftime("%m-%d-%Y")
        cur.execute(insert_query, (team1, team2, team1_score, team2_score, today))
        conn.commit()
        await ctx.send(embed=get_success_embed('addmatch'))
    else:
        await ctx.send(embed=get_nopermission_embed())

@bot.command()
# ROLES = Captain, Coach, Moderator, Operations
async def deletelastmatch(ctx, team):
    captain_role = discord.utils.get(ctx.guild.roles, name="Captains")
    coach_role = discord.utils.get(ctx.guild.roles, name="Coaches")
    moderator_role = discord.utils.get(ctx.guild.roles, name="Moderator")
    ops_role = discord.utils.get(ctx.guild.roles, name="Operations")
    if (captain_role in ctx.author.roles or coach_role in ctx.author.roles or moderator_role in ctx.author.roles or ops_role in ctx.author.roles):
        # Get all matches for team, get the dates, split by -, year->month->day
        getdata_query = "SELECT * FROM match_history WHERE team_one = '" + team + "' OR team_two = '" + team + "';"
        cur.execute(getdata_query)
        matchData = cur.fetchall()
        mostRecentGame = ""
        for row in matchData:
            gameDate = row[4]
            if mostRecentGame == "":
                mostRecentGame = gameDate
            else:
                gameDateInfo = gameDate.split("-") # [MM, DD, YYYY]
                mostRecentGameInfo = mostRecentGame.split("-")
                gameMonth = int(gameDateInfo[0])
                gameDay = int(gameDateInfo[1])
                gameYear = int(gameDateInfo[2])
                # Compare the year first
                if (gameYear == mostRecentGameInfo[2]):
                    # Compare the month next
                    if (gameMonth == mostRecentGameInfo[0]):
                        # Compare the date last
                        if (gameDay >= mostRecentGameInfo[1]):
                            mostRecentGame = gameDate
                    elif (gameMonth > mostRecentGameInfo[0]):
                        mostRecentGame = gameDate
                elif (gameYear > mostRecentGameInfo[2]):
                    mostRecentGame = gameDate
        # At this point, mostRecentGame should be the date we want to remove for team
        # ERROR HANDLE: Check to make sure a game was found
        if (mostRecentGame != ""):
            delete_query = "DELETE FROM match_history WHERE (team_one = '" + team + "' OR team_two = '" + team + "') AND date = '" + mostRecentGame + "';"
            cur.execute(delete_query)
            conn.commit()
            await ctx.send(embed=get_success_embed("deletelastmatch " + team))
        else:
            await ctx.send(embed=get_nodata_embed())
    else:
        await ctx.send(embed=get_nopermission_embed())

@bot.command()
# ROLES: Operations
async def reset(ctx):
    ops_role = discord.utils.get(ctx.guild.roles, name="Operations")
    if (ops_role in ctx.author.roles):
        # Delete entries
        delete_all_query = "DELETE FROM match_history"
        cur.execute(delete_all_query)
        conn.commit()
        await ctx.send(embed=get_reset_embed())
    else:
        await ctx.send(embed=get_nopermission_embed())

@bot.command()
# ROLES: Everyone
async def getdata(ctx, team):
    getdata_query = "SELECT * FROM match_history WHERE team_one = '" + team + "' OR team_two = '" + team + "';"
    cur.execute(getdata_query)
    matchData = cur.fetchall()
    embed = get_results_embed()
    dataFoundFlag = False
    for row in matchData:
        dataFoundFlag = True
        team1 = row[0]
        team2 = row[1]
        team1_score = row[2]
        team2_score = row[3]
        gameDate = row[4]
        field_header = team1 + " " + str(team1_score) + "-" + str(team2_score) + " " + team2
        embed.add_field(name=field_header, value=gameDate, inline=False)
    if (dataFoundFlag):
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=get_nodata_embed())

@bot.command()
# ROLES: Everyone
async def getmatchupdata(ctx, team1, team2):
    getdata_query = "SELECT * FROM match_history WHERE (team_one = '" + team1 + "' AND team_two = '" + team2 + "') OR (team_one = '" + team2 + "' AND team_two = '" + team1 + "')"
    cur.execute(getdata_query)
    matchupData = cur.fetchall()
    embed = get_results_embed()
    dataFoundFlag = False
    for row in matchupData:
        dataFoundFlag = True
        t1 = row[0]
        t2 = row[1]
        team1_score = row[2]
        team2_score = row[3]
        gameDate = row[4]
        field_header = t1 + " " + str(team1_score) + "-" + str(team2_score) + " " + t2
        embed.add_field(name=field_header, value=gameDate, inline=False)
    if (dataFoundFlag):
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=get_nodata_embed())

bot.run('TOKEN HERE') # Replace with bot token