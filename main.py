# bot.py
# local imports
from admin import Admin
from cogs import Games
from sql import SQL
from song import Song

# builtin imports
import asyncio
import os
import random
from datetime import datetime

# discord imports
import discord
from dotenv import load_dotenv
from discord.ext import commands

# database
import mysql.connector

load_dotenv()
TOKEN = os.environ["TOKEN"]  # taking environment variables from .env
PASSWORD = os.environ["PASSWORD"]
USER = os.environ["USR"]
HOST = os.environ["HOST"]
DATABASE = os.environ["DATABASE"]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)  # creates bot instance

lvls = mysql.connector.connect(user = USER,
                               password = PASSWORD,
                               host = HOST,
                               database = DATABASE)

cursor = lvls.cursor()
sql = SQL(cursor, lvls)

LIGHTPINK = 0xff85a2

@bot.event
async def on_ready():
    print('{} is on'.format(
        bot.user.name))  # gives notification when bot is online and sets game message to "Playing with Axolotls"
    await bot.change_presence(activity=discord.Game(name='with Axolotls'))
    roles = bot.get_channel(797867864593006592)

    reactionmessage = """:triangular_ruler: - precalc\n
                         :book: - ela (thompson)\n
                         :tools: - ied\n
                         :straight_ruler: - algebra 2\n
                         :earth_americas: - world history\n
                         :blue_square: - salem\n
                         :black_large_square: - plymouth\n
                         :red_square: - canton\n
                         :loudspeaker: - announcements\n
                         :man_scientist: - biology\n
                         :flag_fr: - french\n
                         :united_nations: - ap world\n
                         :closed_book: - ela (wright)\n"""

    reactionembed = discord.Embed(title="react to the following emojis for ur roles", description=reactionmessage)

    message = await roles.send(embed=reactionembed)

    emojis = ['📐', '📖', '🛠️', '📏', '🌎', '🟦', '⬛', '🟥', '📢', '👨‍🔬', '🇫🇷', '🇺🇳', '📕']
    for emoji in emojis:
        await message.add_reaction(emoji)

    reactionmessage = """:computer: - cse\n
                        :robot: - robotics\n
                        :rocket: - physics (gell)\n
                        :airplane_departure: - physics (hiske)\n
                        :flag_es: - spanish 2\n
                        :flag_mx: - spanish 3\n
                        :heavy_division_sign: - math olympiad\n"""

    reactionembed = discord.Embed(description=reactionmessage)

    message = await roles.send(embed=reactionembed)

    emojis = ['💻', '🤖', '🚀', '🛫', '🇪🇸', '🇲🇽', '➗']
    for emoji in emojis:
        await message.add_reaction(emoji)


@bot.event
async def on_message(message):
    main = bot.get_channel(763475634278105088)
    mutedchat = bot.get_channel(766656875256741898)
    spam = bot.get_channel(768876717422936115)
    music = bot.get_channel(757970344496726025)  # channel declarations
    gulag = bot.get_channel(788434232401461248)
    joinrole = bot.get_channel(765560283116208158)
    relay = bot.get_channel(798991401102475384)
    adminlogs = bot.get_channel(800417369548914708)
    timeout = bot.get_channel(785898040254922784)
    
    axolotlclan = bot.get_guild(591065297692262410)  # guild declarations

    vip = discord.utils.get(axolotlclan.roles, name="VIP")  # accesses the role vip, and adds it to the user
    mvp = discord.utils.get(axolotlclan.roles, name="MVP")
    no_media = discord.utils.get(axolotlclan.roles, name="no media")

    bannedchannels = [mutedchat, spam, music, gulag, joinrole, timeout]  # makes lists of blacklisted channels
    images = ['.jpg', '.png', '.jpeg', '.gif']

    user = message.author
    id = str(user.id)

    if user.bot:
        return

    if "axolotl bot is bad" in message.content.lower():  # triggers on the message "axolotl bot is bad"
        # await user.create_dm()      #starts a "channel" which is actually just a dm
        await user.send(
            "buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL"
        )
        await user.send(file=discord.File('buffaxolotl.png'))  # threatening dm

    if "school sucks" in message.content.lower():  # triggers on the message "school sucks"
        authorping = '<@' + id + '>'  # creates a ping message

        msgs = []  # creates empty list to log the pings
        for _ in range(5):  # iterate 5 times
            sent_message = await user.send(authorping)  # ping the person in dm channel
            msgs.append(sent_message)  # log the message

        for message in msgs:  # iterate through all the sent messages
            await message.delete()  # delete them

    if message.channel == relay and message.content[0] != "@":
        await main.send(message.content)
    if message.channel == main:
        relaymessage = user.name + ": " + message.content
        await relay.send(relaymessage)
    if no_media in user.roles:
        deleteEmbed = discord.Embed(color=LIGHTPINK, timestamp=datetime.utcnow())
        deleteEmbed.title = f"i deleted media sent by {user.name} in {message.channel}"
        if "https://" in message.content:
            await message.delete()
            await adminlogs.send(embed=deleteEmbed)
        if message.attachments:
            url = message.attachments[0].url
            for ext in images:
                if url.endswith(ext):
                    await message.delete()
                    await adminlogs.send(embed=deleteEmbed)
                    return

    if len(message.content) == 0:
        return

    if message.channel not in bannedchannels and message.content[0] != "." and message.content[0] != "?" and message.content[0] != "!":  # check if it's not a spam channel or a bot command
        if not sql.checkExist(id):  # if a new user joins and says something, create a new dictionary in the json file
            sql.cursor.execute(f"INSERT INTO levels VALUES ({id}, '1', '1')")
            lvls.commit()

        else:
            if 100 * (sql.getLevel(id) - 1) + 50 <= sql.getXP(id)+ 1: # check if it passed the level; level cap is calculated as 100 * (level - 1) + 50
                sql.editLevel(id, 1)
                sql.editXP(id, -sql.getXP(id))

                levelUP = str(user.name) + " leveled up to " + str(sql.getLevel(id)) + "!"  # create level up message
                levelupembed = discord.Embed(title=levelUP, color=LIGHTPINK)  # create embed with level up message
                await message.channel.send(embed=levelupembed)  # send embed

                if sql.getLevel(id) >= 10 and vip not in user.roles:
                    viprank = str("congrats, you earned the VIP role!")
                    vipembed = discord.Embed(title=viprank, color=LIGHTPINK)  # vip embed once they reach level 25
                    await message.channel.send(embed=vipembed)
                    await user.add_roles(vip)

                if sql.getLevel(id) >= 20 and mvp not in user.roles:
                    mvprank = str("congrats, you earned the MVP role!")
                    mvpembed = discord.Embed(title=mvprank, color=LIGHTPINK)
                    await message.channel.send(embed=mvpembed)
                    await user.add_roles(mvp)

            else:  # any message sent
                added_xp = random.randint(1, 5)  # xp randomized from 1-5, may change later
                sql.editXP(id, added_xp) # increase the xp by the randomized xp

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):  # triggers on member join
    main = bot.get_channel(763475634278105088)

    await member.send(
        f"Hi, {member.name}, welcome to Axolotl Clan!\nMake sure to look at the <#763387839522013194> and "
        f"<#758025770181460015>\nUse the school roles channel to get your class or game roles!")  # welcome and
    # informational message
    await main.send(f"{member.name} is here!")


@bot.event
async def on_reaction_add(reaction, user):
    roles = bot.get_channel(797867864593006592)
    axolotl = bot.get_user(791048344956043274)
    axolotlclan = bot.get_guild(591065297692262410)

    emojiRoles = {'📐': 'Precalc', '📖': 'ELA (Thompson)', '🛠️': 'IED', '📏': 'Algebra 2', '🌎': 'World History',
                  '🟦': 'Salem', '⬛': 'Plymouth', '🟥': 'Canton', '📢': 'Announcements', '👨‍🔬': 'Biology',
                  '🇫🇷': 'French',
                  '🇺🇳': 'AP World', '📕': 'ELA (Wright)', '💻': 'CSE', '🤖': 'Robotics',
                  '🚀': 'Physics (Gell)', '🛫': 'Physics (Hiske)', '🇪🇸': 'Spanish 2', '🇲🇽': 'Spanish 3',
                  '➗': 'Math Olympiad'}

    if reaction.message.channel != roles:
        return
    elif user == axolotl:
        return
    else:
        role = discord.utils.get(axolotlclan.roles, name=emojiRoles[str(reaction)])
        if role in user.roles:
            await user.remove_roles(role)
            await user.send('you were removed from the ' + role.name + ' role in axolotl clan')
        else:
            await user.add_roles(role)
            await user.send('you got the ' + role.name + ' role in axolotl clan')
        await reaction.remove(user)


@bot.command(aliases=['lvl', 'level'], help="Displays someones level in axolotl clan")
async def _level(ctx, user: discord.Member):
    spam = bot.get_channel(768876717422936115)
    id = str(user.id)
    if ctx.channel == spam:
        if sql.checkExist(id):
            level = "level: " + str(sql.getLevel(id)) + "\n"  # accesses the level of the person who sent it from the json file.
            msgs = "xp: " + str(sql.getXP(id)) + "/" + str(100 * (sql.getLevel(id) - 1) + 50)  # accesses the xp needed from the json file, (current xp/needed xp)

            levelinfoembed = discord.Embed(title=level + msgs, color=LIGHTPINK,timestamp=datetime.utcnow())  # creates embed of levels (and sets a timestamp)
            levelinfoembed.set_footer(text='Retrieved Data')

            await ctx.send(embed=levelinfoembed)
        else:
            levelinfoembed = discord.Embed(title="I couldn't find that user, try mentioning them instead", color=LIGHTPINK, timestamp=datetime.utcnow())
            await ctx.send(embed=levelinfoembed)
        
@bot.command(name='invites', help='checks how many invites you have, if you have three or higher you get vip')
async def _invites(ctx):
    axolotlclan = bot.get_guild(591065297692262410)
    message = ctx.message
    user = message.author

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    invitesmessage = f"You've invited {totalInvites} member(s) to the server!"
    invitesEmbed = discord.Embed(title=invitesmessage, color=LIGHTPINK, timestamp=datetime.utcnow())

    vip = discord.utils.get(axolotlclan.roles, name="VIP")  # accesses the role vip, and adds it to the user
    if totalInvites >= 3 and vip not in ctx.author.roles:
        viprank = str("congrats, you earned the VIP role!")
        vipembed = discord.Embed(title=viprank, color=LIGHTPINK)  # vip embed once they reach level 25
        await message.channel.send(embed=vipembed)

        await user.add_roles(vip)

    await ctx.send(embed=invitesEmbed)


@bot.command(name='ping', help="pings someone 5 times")
@commands.has_role('Admin')
async def _ping(ctx, user: discord.Member):
    for _ in range(5):
        await ctx.send(user.mention)


@bot.command(name="setlevel", help="sets someone level to specific number")
@commands.has_role('Admin')
async def _setlevel(ctx, *args):
    foundUser = False
    if len(args) != 2:
        await ctx.send("invalid format, please do .setlevel (user) (level)")
        return
    elif int(args[1]) < 0:
        await ctx.send("you can't have a negative level")
        return
    else:
        for user in ctx.guild.members:
            if args[0] == user.name:
                sql.editLevel(str(user.id), int(args[1]) - sql.getLevel(str(user.id)))

                await ctx.send(f"set **{user.name}**'s level to {args[1]}")
                foundUser = True
                break
    if not foundUser:
        await ctx.send("could not find that user")


@bot.command(aliases=["lb", "leaderboard"])
async def _leaderboard(ctx):
    rawxpleaderboard = []
    rawxpdictionary = {}
    leaderboard = []

    for user in sql.getIDs():
        person = bot.get_user(int(user))

        if not person.bot:
            rawxp = (100 * (sql.getLevel(user) - 2) + 100) * (sql.getLevel(user) - 1) / 2 + sql.getXP(user)
            rawxpleaderboard.append(rawxp)
            rawxpdictionary[rawxp] = person

    rawxpleaderboard.sort(reverse=True)

    for i in range(20):
        usr = rawxpdictionary[rawxpleaderboard[i]]
        userLevel = sql.getLevel(usr.id)
        userXP = sql.getXP(usr.id)
        leaderboard.append(f"{i + 1}. {usr.name}'s raw xp: **{int(rawxpleaderboard[i])}** | level: **{userLevel}** | xp: **{userXP}**")

    lbString = ""
    for place in leaderboard:
        lbString += place + "\n"

    lbEmbed = discord.Embed(title="Top 20 for Axolotl Clan:", color=LIGHTPINK, timestamp=datetime.utcnow())
    lbEmbed.description = lbString
    lbEmbed.set_footer(text="Axolotl Clan")
    await ctx.send(embed=lbEmbed)

@bot.command(name = "balls", help = "Gives Arav 10000 xp")
@commands.cooldown(1, 10, commands.BucketType.user)
async def balls(ctx):
    spam = bot.get_channel(768876717422936115)
    if ctx.channel == spam:
        ball = discord.Embed(title = "Gave Arav 10000 xp", color = LIGHTPINK, timestamp = datetime.utcnow())
        await ctx.send(embed = ball)
    else:
        await ctx.send("Go to spam smh my head")

@balls.error
async def balls_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(error)


bot.add_cog(Games(bot))
bot.add_cog(Admin(bot))
bot.add_cog(Song(bot))

bot.run(TOKEN)  # runs the program
