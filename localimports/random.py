# admin.py
# discord imports
import discord
from discord.ext import commands
from datetime import datetime

import random

DARKPINK = 0xe75480

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='rm', help="gets a random message that's been previously sent in main")
    async def rm(self, ctx):
        f = open("localimports/PREPPEDAXOTXT.txt", "r")
        m = f.readlines()
        await ctx.send(m[random.randint(0, len(m))])