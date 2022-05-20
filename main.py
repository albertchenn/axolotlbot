# bot.py
# local imports
from localimports.admin import Admin
from localimports.game import Games
from localimports.sql import SQL
from localimports.levels import Levels
from localimports.random import Random

# builtin imports
import asyncio
import os
import random
from datetime import datetime

# discord imports
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.environ["TOKEN"]  # taking environment variables from .env

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=";", intents=intents)  # creates bot instance

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

    PJ = '591065108210384896' # The special PJ ID

    bannedchannels = [spam, music, timeout]  # makes lists of blacklisted channels
    images = ['.jpg', '.png', '.jpeg', '.gif']
    bannedstarts = ['!', '.', '?']
    pingchannels = [main, media, spam]
    
    axolotlclan = bot.get_guild(591065297692262410)  # guild declarations

    vip = discord.utils.get(axolotlclan.roles, id=796851771510095882)  # accesses the role vip, and adds it to the user
    mvp = discord.utils.get(axolotlclan.roles, id=804063860104495134)
    no_media = discord.utils.get(axolotlclan.roles, id=804007659229544449)    
    admin = discord.utils.get(axolotlclan.roles, id=769171897564004362)

    user = message.author
    id = str(user.id)


    if user.bot or (message.channel == discord.channel.DMChannel):
        return

    if len(message.content) == 0:
        return

    await bot.process_commands(message)

bot.add_cog(Random(bot))

bot.run(TOKEN)  # runs the program
