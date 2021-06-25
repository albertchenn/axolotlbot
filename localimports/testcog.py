# admin.py
# discord imports
import discord
from discord.ext import commands
from datetime import datetime

from discord_slash import cog_ext
from discord_slash.context import ComponentContext
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

DARKPINK = 0xe75480
guild_ids = [591065297692262410]

class Test(commands.Cog):
    def __init__(self, bot, sql):
        self.bot = bot
        self.sql = sql
        self.buttons = [manage_components.create_button(style=ButtonStyle.green, label = "SUSSY AMOGUS")]
        self.action_row = manage_components.create_actionrow(*self.buttons)
    
    @cog_ext.cog_slash(name='amogus', description="sussy baka", guild_ids=guild_ids)
    async def amogus(self, ctx):
        await ctx.send("green gamer is sussy :happy:")


