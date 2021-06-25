# bot.py
# local imports
from localimports.admin import Admin
from localimports.adminslash import AdminSlash
from localimports.game import Games
from localimports.sql import SQL
from localimports.song import Song
from localimports.levels import Levels
from localimports.levelsslash import LevelsSlash
from localimports.testcog import Test 

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

from discord_slash import SlashCommand

load_dotenv()
TOKEN = os.environ["TOKEN"]  # taking environment variables from .env
PASSWORD = os.environ["MYSQLPASSWORD"]
USER = os.environ["MYSQLUSER"]
HOST = os.environ["MYSQLHOST"]
DATABASE = os.environ["MYSQLDATABASE"]
PORT = os.environ["MYSQLPORT"]

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)  # creates bot instance
slash = SlashCommand(bot, sync_commands=True)

lvls = mysql.connector.connect(user = USER,
                               password = PASSWORD,
                               host = HOST,
                               database = DATABASE,
                               port = PORT)

cursor = lvls.cursor()
sql = SQL(cursor, lvls)

LIGHTPINK = 0xff85a2

guild_ids = [591065297692262410]

@bot.event
async def on_ready():
    print('{} is on'.format(bot.user.name))  # gives notification when bot is online and sets game message to "Playing with Axolotls"
    await bot.change_presence(activity=discord.Game(name='with Axolotls'))

@bot.event
async def on_message(message):
    main = bot.get_channel(763475634278105088)
    media = bot.get_channel(765571073043333171)
    spam = bot.get_channel(768876717422936115)
    music = bot.get_channel(757970344496726025)  # channel declarations
    relay = bot.get_channel(798991401102475384)
    adminlogs = bot.get_channel(800417369548914708)
    timeout = bot.get_channel(785898040254922784)

    bannedchannels = [spam, music, timeout]  # makes lists of blacklisted channels
    images = ['.jpg', '.png', '.jpeg', '.gif']
    bannedstarts = ['!', '.', '?']
    pingchannels = [main, media, spam]
    
    axolotlclan = bot.get_guild(591065297692262410)  # guild declarations

    vip = discord.utils.get(axolotlclan.roles, id=796851771510095882)  # accesses the role vip, and adds it to the user
    mvp = discord.utils.get(axolotlclan.roles, id=804063860104495134)
    no_media = discord.utils.get(axolotlclan.roles, id=804007659229544449)    
    
    user = message.author
    id = str(user.id)

    if user.bot or (message.channel == discord.channel.DMChannel):
        return

    if "axolotl bot is bad" in message.content.lower():  # triggers on the message "axolotl bot is bad"
        # await user.create_dm()      #starts a "channel" which is actually just a dm
        await user.send(
            "buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL"
        )
        await user.send(file=discord.File('images/buffaxolotl.png'))  # threatening dm

    if "school sucks" in message.content.lower():  # triggers on the message "school sucks"
        msgs = []  # creates empty list to log the pings
        for _ in range(5):  # iterate 5 times
            channel = random.choice(pingchannels)
            sent_message = await channel.send(user.mention)  # ping the person in dm channel
            msgs.append(sent_message)  # log the message

        for message in msgs:  # iterate through all the sent messages
            await message.delete()  # delete them

    if message.channel == relay and "@" not in message.content:
        await main.send(message.content)
    if message.channel == main and "@" not in message.content:
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

    if (message.channel not in bannedchannels) and (message.content[0] not in bannedstarts) and (message.guild.id == axolotlclan.id):  # check if it's not a spam channel or a bot command
        if not sql.checkExist(id):  # if a new user joins and says something, create a new dictionary in the json file
            sql.addNewUser(id)

        else:
            if 100 * sql.getLevel(id) - 50 <= sql.getXP(id)+ 1: # check if it passed the level; level cap is calculated as 100 * (level - 1) + 50
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

@slash.slash(name = "test", guild_ids = guild_ids)
async def test(ctx):
    await ctx.send("<@435185747184582668>")

bot.add_cog(Games(bot))
bot.add_cog(Song(bot))
bot.add_cog(Admin(bot, sql))
bot.add_cog(AdminSlash(bot, sql))
bot.add_cog(Levels(bot, sql))
bot.add_cog(LevelsSlash(bot, sql))
bot.add_cog(Test(bot, sql))

bot.run(TOKEN)  # runs the program
