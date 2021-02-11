# bot.py
from admin import Admin
import asyncio
import os
import json  # python imports
import random
from datetime import datetime
from cogs import Games

import discord
from dotenv import load_dotenv  # discord imports
from discord.ext import commands

with open('levels.json', 'r') as f:
    levels = json.load(f)  # takes the json file and makes it a "levels" dictionary

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # taking environment variables from .env

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)  # creates bot instance


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

    axolotlclan = bot.get_guild(591065297692262410)  # guild declarations

    vip = discord.utils.get(axolotlclan.roles, name="VIP")  # accesses the role vip, and adds it to the user
    mvp = discord.utils.get(axolotlclan.roles, name="MVP")
    no_media = discord.utils.get(axolotlclan.roles, name="no media")

    bannedchannels = [mutedchat, spam, music, gulag, joinrole]  # makes lists of blacklisted channels
    images = ['.jpg', '.png', '.jpeg', '.gif']

    if message.author.bot:
        return

    if "axolotl bot is bad" in message.content.lower():  # triggers on the message "axolotl bot is bad"
        # await message.author.create_dm()      #starts a "channel" which is actually just a dm
        await message.author.send(
            "buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL"
        )
        await message.author.send(file=discord.File('buffaxolotl.png'))  # threatening dm

    if "school sucks" in message.content.lower():  # triggers on the message "school sucks"
        authorid = str(message.author.id)  # finds the person's id
        authorping = '<@' + authorid + '>'  # creates a ping message

        msgs = []  # creates empty list to log the pings
        for _ in range(5):  # iterate 5 times
            sent_message = await message.author.send(authorping)  # ping the person in dm channel
            msgs.append(sent_message)  # log the message

        for message in msgs:  # iterate through all the sent messages
            await message.delete()  # delete them

    if message.channel == relay and message.content[0] != "@":
        await main.send(message.content)
    if message.channel == main:
        relaymessage = message.author.name + ": " + message.content
        relaymessageembed = discord.Embed(title=relaymessage)
        await relay.send(embed=relaymessageembed)
    if no_media in message.author.roles:
        deleteEmbed = discord.Embed(color=0xff85a2, timestamp=datetime.utcnow())
        deleteEmbed.title = f"i deleted media sent by {message.author.name} in {message.channel}"
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

    if message.channel not in bannedchannels and message.content[0] != "." and message.content[0] != "?" and \
            message.content[0] != "!":  # check if it's not a spam channel or a bot command
        if str(
                message.author.id) not in levels:  # if a new user joins and says something, create a new dictionary
            # in the json file
            levels[str(message.author.id)] = {"xp": 1, "level": 1}
            print('new user')  # debugging

        else:
            if 100 * (levels[str(message.author.id)]["level"] - 1) + 50 <= levels[str(message.author.id)]["xp"] + 1:
                # check if it passed the level; level cap is calculated as 100 * (level - 1) + 50
                levels[str(message.author.id)]["level"] += 1  # increase level by one
                levels[str(message.author.id)]["xp"] = 0  # reset xp
                levelUP = str(message.author.name) + " leveled up to " + str(
                    levels[str(message.author.id)]["level"]) + "!"  # create level up message
                levelupembed = discord.Embed(title=levelUP, color=0xFFC0CB)  # create embed with level up message
                await message.channel.send(
                    embed=levelupembed)  # send embed; YOU HAVE TO SEND THE EMBED FOR IT TO REGISTER

                if levels[str(message.author.id)]["level"] >= 10 and vip not in message.author.roles:
                    viprank = str("congrats, you earned the VIP role!")
                    vipembed = discord.Embed(title=viprank, color=0xff85a2)  # vip embed once they reach level 25
                    await message.channel.send(embed=vipembed)
                    await message.author.add_roles(vip)
                elif levels[str(message.author.id)]["level"] >= 20 and mvp not in message.author.roles:
                    mvprank = str("congrats, you earned the MVP role!")
                    mvpembed = discord.Embed(title=mvprank, color=0xff85a2)
                    await message.channel.send(embed=mvpembed)
                    await message.author.add_roles(mvp)
            else:  # any message sent
                added_xp = random.randint(1, 5)  # xp randomized from 1-5, may change later
                levels[str(message.author.id)]["xp"] += added_xp  # increase the xp by the randomized xp
        with open('levels.json', 'w') as a:
            a.write(json.dumps(levels, indent=4,
                               sort_keys=True))  # save the dictionary of dictionaries of levels and xp to "levels.json"
        a.close()

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
    if ctx.channel == spam:
        if str(user.id) in levels:
            level = "level: " + str(levels[str(user.id)][
                                        "level"]) + "\n"  # accesses the level of the person who sent it from the
            # json file.
            msgs = "xp: " + str(levels[str(user.id)]["xp"]) + "/" + str(100 * (levels[str(user.id)][
                                                                                   "level"] - 1) + 50)  # accesses
            # the xp needed from the json file, (current xp/needed xp)

            levelinfoembed = discord.Embed(title=level + msgs, color=0xff85a2,
                                           timestamp=datetime.utcnow())  # creates embed of levels (and sets a
            # timestamp)
            levelinfoembed.set_footer(text='Retrieved Data')

            await ctx.send(embed=levelinfoembed)
        else:
            levelinfoembed = discord.Embed(title="I couldn't find that user, try mentioning them instead",
                                           color=0xff85a2, timestamp=datetime.utcnow())
            await ctx.send(embed=levelinfoembed)


@bot.command(aliases=['play', 'p'], help="plays an mp3 song, do .playsong for more info")
@commands.has_role('VIP')
async def _play(ctx, *args):
    user = ctx.author
    vc = user.voice.channel
    songs = ["pog", "pogU", "Wait", "what", "manhunt", "bestsong", "men", "pathetique", "arabesque"]
    if vc is None:
        await ctx.send("please join a vc before using this command")

    elif len(args) == 0:
        await ctx.send('the songs that are currently available are: ' + str(songs))
        return

    elif args[0] in songs:
        if vc is not None:
            voice_channel = await vc.connect()
            channel = vc.name
            await ctx.send(user.name + " is in " + channel)
            await ctx.send("do '.stop' to stop the song, (you have to make it leave for it to play another song)")
            if len(args) == 1:
                voice_channel.play(discord.FFmpegPCMAudio("songs/" + args[0] + ".mp3"))
                while voice_channel.is_playing():
                    await asyncio.sleep(1)

            if args[1] == "loop":
                await ctx.send("you have chosen the 'loop' switch, it will play endlessly unless you stop it.")
                while True:
                    voice_channel.play(discord.FFmpegPCMAudio("songs/" + args[0] + ".mp3"))
                    while voice_channel.is_playing():
                        await asyncio.sleep(1)
            voice_channel.stop()
        else:
            await ctx.send('User is not in a channel')

    elif args[0] == "all":
        voice_channel = await vc.connect()
        channel = vc.name
        await ctx.send("user is in " + channel)
        await ctx.send("do '.stop' to stop the song, (you have to make it leave for it to play another song)")
        for song in songs:
            voice_channel.play(discord.FFmpegPCMAudio("songs/" + song + ".mp3"))
            while voice_channel.is_playing():
                await asyncio.sleep(1)
    else:
        await ctx.send("could not find that song")


@bot.command(name='stop', help='leaves the vc')
async def _stop(ctx):
    user = ctx.author
    vc = user.voice.channel

    if vc is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("axolotl has left the vc")
    else:
        await ctx.send('User is not in a channel')


@bot.command(name='invites', help='checks how many invites you have, if you have three or higher you get vip')
async def _invites(ctx):
    axolotlclan = bot.get_guild(591065297692262410)
    message = ctx.message

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    invitesmessage = f"You've invited {totalInvites} member(s) to the server!"
    invitesEmbed = discord.Embed(title=invitesmessage, color=0xff85a2, timestamp=datetime.utcnow())

    vip = discord.utils.get(axolotlclan.roles, name="VIP")  # accesses the role vip, and adds it to the user
    if totalInvites >= 3 and vip not in ctx.author.roles:
        viprank = str("congrats, you earned the VIP role!")
        vipembed = discord.Embed(title=viprank, color=0xff85a2)  # vip embed once they reach level 25
        await message.channel.send(embed=vipembed)

        await message.author.add_roles(vip)

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
                levels[str(user.id)] = {"xp": 1, "level": int(args[1])}
                await ctx.send(f"set **{user.name}**'s level to {args[1]}")
                foundUser = True
                break
    if not foundUser:
        await ctx.send("could not find that user")

    with open('levels.json', 'w') as b:
        b.write(json.dumps(levels, indent=4,
                           sort_keys=True))  # save the dictionary of dictionaries of levels and xp to "levels.json"
    b.close()


@bot.command(aliases=["lb", "leaderboard"])
async def _leaderboard(ctx):
    rawxpleaderboard = []
    rawxpdictionary = {}
    leaderboard = []
    for user in levels:
        person = bot.get_user(int(user))
        if not person.bot:
            # leaderboard.append(f"{person.name}: level {levels[user]['level']} at {levels[user]['xp']} xp")
            rawxp = (100 * (levels[user]['level'] - 1) - 1) * (levels[user]["level"]) / 2 + levels[user]["xp"]
            rawxpleaderboard.append(rawxp)
            rawxpdictionary[rawxp] = person

    rawxpleaderboard.sort(reverse=True)

    for i in range(20):
        User = rawxpdictionary[rawxpleaderboard[i]]
        userLevel = levels[str(User.id)]["level"]
        userXP = levels[str(User.id)]["xp"]
        leaderboard.append(f"{i + 1}. {User.name}'s raw xp: **{rawxpleaderboard[i]}** | level: **{userLevel}** | xp: **{userXP}**")

    lbString = ""
    for place in leaderboard:
        lbString += place + "\n"

    lbEmbed = discord.Embed(title="Top 20 for Axolotl Clan:", color=0xff85a2, timestamp=datetime.utcnow())
    lbEmbed.description = lbString
    lbEmbed.set_footer(text="Axolotl Clan")
    await ctx.send(embed=lbEmbed)


bot.add_cog(Games(bot))
bot.add_cog(Admin(bot))

bot.run(TOKEN)  # runs the program
