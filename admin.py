# admin.py
# discord imports
import discord
from discord.ext import commands
from datetime import datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='mute', help="mutes them")
    @commands.has_any_role('Admin', 'Moderator', 'Trial Moderator')
    async def mute(self, ctx, user: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name = 'Muted')
        logs = self.bot.get_channel(800417369548914708)
        alreadyMuted = None

        mutedEmbed = discord.Embed(color=0xe75480, timestamp=datetime.utcnow()) 
        if muted in user.roles:
            mutedEmbed.title = "the user is already muted"
            alreadyMuted = True
        else:
            await user.add_roles(muted)
            mutedEmbed.title = f"{user.name} was muted"

        await ctx.send(embed = mutedEmbed)
        if not alreadyMuted:
            await logs.send(f"{ctx.author.name} muted {user.name}")

    @commands.command(name='unmute', help="unmutes them")
    @commands.has_any_role('Admin', 'Moderator', "Trial Moderator")
    async def unmute(self, ctx, user: discord.Member):
        muted = discord.utils.get(ctx.guild.roles, name = 'Muted')

        unmuteEmbed = discord.Embed(color = 0xe75480, timestamp=datetime.utcnow())
        if muted not in user.roles:
            unmuteEmbed.title = "the user is already unmuted"
        else:
            await user.remove_roles(muted)
            unmuteEmbed.title = f"{user.name} was unmuted"

        await ctx.send(embed = unmuteEmbed)

    @commands.command(name='timeout', help="put them in timeout(reduce the amount of channels they see")
    @commands.has_any_role('Admin', 'Moderator', 'Trial Moderator')
    async def timeout(self, ctx, user: discord.Member):
        member = discord.utils.get(ctx.guild.roles, name = 'Member')

        timeoutEmbed = discord.Embed(color = 0xe75480, timestamp = datetime.utcnow())
        if member not in user.roles:
            timeoutEmbed.title = "the user is already in timeout"
        else:
            await user.remove_roles(member)
            timeoutEmbed.title = f"{user.name} was sent to timeout"

        await ctx.send(embed=timeoutEmbed)
    
    @commands.command(name='timein', help="un timeouts them")
    @commands.has_any_role('Admin', 'Moderator', 'Trial Moderator')
    async def timein(self, ctx, user: discord.Member):
        member = discord.utils.get(ctx.guild.roles, name = 'Member')

        timeinEmbed = discord.Embed(color = 0xe75480, timestamp = datetime.utcnow())
        if member in user.roles:
            timeinEmbed.title = "the user is already out of timeout"
        else:
            await user.add_roles(member)
            timeinEmbed.title = f"{user.name} was sent out of timeout"

        await ctx.send(embed=timeinEmbed)

    @commands.command(name='mediamute', help="mutes them from media")
    @commands.has_any_role('Admin', 'Moderator', 'Trial Moderator')
    async def mediamute(self, ctx, user: discord.Member):
        mediamute = discord.utils.get(ctx.guild.roles, name = 'no media')

        mediamuteEmbed = discord.Embed(color = 0xe75480, timestamp = datetime.utcnow())
        if mediamute in user.roles:
            mediamuteEmbed.title = "that user is already muted from media"
        else:
            mediamuteEmbed.title = f"{user.name} was muted from sending media"
            await user.add_roles(mediamute)
        
        await ctx.send(embed=mediamuteEmbed)

    @commands.command(name='mediaunmute', help="unmutes them from media")
    @commands.has_any_role('Admin', 'Moderator', 'Trial Moderator')
    async def mediaunmute(self, ctx, user: discord.Member):
        unmediamute = discord.utils.get(ctx.guild.roles, name = 'no media')

        unmediamuteEmbed = discord.Embed(color = 0xe75480, timestamp = datetime.utcnow())
        if unmediamute not in user.roles:
            unmediamuteEmbed.title = "that user is already unmuted from media"
        else:
            unmediamuteEmbed.title = f"{user.name} was unmuted from sending media"
            await user.remove_roles(unmediamute)
        
        await ctx.send(embed=unmediamuteEmbed)
    
