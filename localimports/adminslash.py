# admin.py
# discord imports
import discord
from discord.ext import commands
from datetime import datetime

from discord_slash import cog_ext

DARKPINK = 0xe75480
guild_ids = [591065297692262410]


class AdminSlash(commands.Cog):
    def __init__(self, bot, sql):
        self.bot = bot
        self.sql = sql
    
    @cog_ext.cog_slash(name='mute', description="mutes them", guild_ids=guild_ids)
    @commands.has_any_role(769171897564004362, 757966937769902262, 765183925886124032)
    async def mute(self, ctx, user: discord.Member):
        muted = ctx.guild.get_role(764878992737828876)
        logs = self.bot.get_channel(800417369548914708)
        alreadyMuted = None

        mutedEmbed = discord.Embed(color=DARKPINK, timestamp=datetime.utcnow()) 
        if muted in user.roles:
            mutedEmbed.title = "the user is already muted"
            alreadyMuted = True
        else:
            await user.add_roles(muted)
            mutedEmbed.title = f"{user.name} was muted"

        await ctx.send(embed = mutedEmbed)
        if not alreadyMuted:
            await logs.send(f"{ctx.author.name} muted {user.name}")

    @cog_ext.cog_slash(name='unmute', description="unmutes them", guild_ids=guild_ids)
    @commands.has_any_role(769171897564004362, 757966937769902262, 765183925886124032)
    async def unmute(self, ctx, user: discord.Member):
        muted = ctx.guild.get_role(764878992737828876)

        unmuteEmbed = discord.Embed(color = DARKPINK, timestamp=datetime.utcnow())
        if muted not in user.roles:
            unmuteEmbed.title = "the user is already unmuted"
        else:
            await user.remove_roles(muted)
            unmuteEmbed.title = f"{user.name} was unmuted"

        await ctx.send(embed = unmuteEmbed)

    @cog_ext.cog_slash(name='mediamute', description="mutes them from media", guild_ids=guild_ids)
    @commands.has_any_role(769171897564004362, 757966937769902262, 765183925886124032)
    async def mediamute(self, ctx, user: discord.Member):
        mediamute = ctx.guild.get_role(804007659229544449)
        
        mediamuteEmbed = discord.Embed(color = DARKPINK, timestamp = datetime.utcnow())
        if mediamute in user.roles:
            mediamuteEmbed.title = "that user is already muted from media"
        else:
            mediamuteEmbed.title = f"{user.name} was muted from sending media"
            await user.add_roles(mediamute)
        
        await ctx.send(embed=mediamuteEmbed)

    @cog_ext.cog_slash(name='mediaunmute', description="unmutes them from media", guild_ids=guild_ids)
    @commands.has_any_role(769171897564004362, 757966937769902262, 765183925886124032)
    async def mediaunmute(self, ctx, user: discord.Member):
        unmediamute = ctx.guild.get_role(804007659229544449)

        unmediamuteEmbed = discord.Embed(color = DARKPINK, timestamp = datetime.utcnow())
        if unmediamute not in user.roles:
            unmediamuteEmbed.title = "that user is already unmuted from media"
        else:
            unmediamuteEmbed.title = f"{user.name} was unmuted from sending media"
            await user.remove_roles(unmediamute)
        
        await ctx.send(embed=unmediamuteEmbed)
    
    @cog_ext.cog_slash(name="setlevel", description="sets someone level to specific number", guild_ids=guild_ids)
    @commands.has_role('Admin')
    async def setlevel(self, ctx, user: discord.Member, level: int):
        if level < 0:
            await ctx.send("you can't have a negative level")
            return
        
        else:
            self.sql.editLevel(str(user.id), level - self.sql.getLevel(str(user.id)))
            await ctx.send(f"set **{user.name}**'s level to {level}")

    @setlevel.error
    async def setlevel_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("format is .setlevel (user) (level)")


    @cog_ext.cog_slash(description="pings someone 5 times", guild_ids=guild_ids)
    @commands.has_role('Admin')
    async def ping(self, ctx, user: discord.Member):
        for _ in range(5):
            await ctx.send(user.mention)
