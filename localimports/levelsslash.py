# admin.py
# discord imports
import discord
from discord.ext import commands
from datetime import datetime

from discord_slash import cog_ext

DARKPINK = 0xe75480
LIGHTPINK = 0xff85a2

guild_ids = [591065297692262410]

class LevelsSlash(commands.Cog):
    def __init__(self, bot, sql):
        self.bot = bot
        self.sql = sql
    
    @cog_ext.cog_slash(name="level", description="Displays someones level in axolotl clan", guild_ids=guild_ids)
    async def level(self, ctx, user: discord.Member = None):
        spam = self.bot.get_channel(768876717422936115)
        if user == None:
            id = str(ctx.author.id)
        else:
            id = str(user.id)
        if ctx.channel == spam:
            if self.sql.checkExist(id):
                level = "level: " + str(self.sql.getLevel(id)) + "\n"  # accesses the level of the person who sent it from the json file.
                msgs = "xp: " + str(self.sql.getXP(id)) + "/" + str(100 * (self.sql.getLevel(id) - 1) + 50)  # accesses the xp needed from the json file, (current xp/needed xp)

                levelinfoembed = discord.Embed(title=level + msgs, color=LIGHTPINK,timestamp=datetime.utcnow())  # creates embed of levels (and sets a timestamp)
                levelinfoembed.set_footer(text='Retrieved Data')

                await ctx.send(embed=levelinfoembed)
            else:
                levelinfoembed = discord.Embed(title="I couldn't find that user, try mentioning them instead", color=LIGHTPINK, timestamp=datetime.utcnow())
                await ctx.send(embed=levelinfoembed)

    @cog_ext.cog_slash(name = "balls", description = "Gives Arav 10000 xp cuz he creams to dream", guild_ids=guild_ids)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def balls(self, ctx):
        spam = self.bot.get_channel(768876717422936115)
        if ctx.channel == spam:
            ball = discord.Embed(title = "Gave Arav 10000 xp", color = LIGHTPINK, timestamp = datetime.utcnow())
            await ctx.send(embed = ball)
        else:
            await ctx.send("Go to spam smh my head")
            
    @cog_ext.cog_slash(name="lb", guild_ids=guild_ids)
    async def lb(self, ctx):
        rawxpdictionary = {}
        leaderboard = []
        await ctx.defer()
        
        for user in self.sql.getIDs():
            person = self.bot.get_user(int(user))
            if not person:
                continue
            if not person.bot: 
                rawxp = 50 * (self.sql.getLevel(user) ** 2) + self.sql.getXP(user)
                rawxpdictionary[person] = rawxp
                rawxpdictionary = dict(sorted(rawxpdictionary.items(), key=lambda item: item[1], reverse=True))

        place = 1
         
        for usr in rawxpdictionary:
            userLevel = self.sql.getLevel(usr.id)
            userXP = self.sql.getXP(usr.id)
            leaderboard.append(f"{place}. {usr.name}'s raw xp: **{int(rawxpdictionary[usr])}** | level: **{userLevel}** | xp: **{userXP}**")
  
            place += 1
            
            if place == 11:
                break
            
        lbString = ""
        for place in leaderboard:
            lbString += place + "\n"

        lbEmbed = discord.Embed(title="Top 10 for Axolotl Clan:", color=LIGHTPINK, timestamp=datetime.utcnow())
        lbEmbed.description = lbString
        lbEmbed.set_footer(text="Axolotl Clan")
        await ctx.send(embed=lbEmbed)

    @cog_ext.cog_slash(description='checks how many invites you have, if you have three or higher you get vip', guild_ids=guild_ids) # ik this isn't the right place but theres no other good spot lmao
    async def invites(self, ctx):
        axolotlclan = self.bot.get_guild(591065297692262410)

        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        invitesmessage = f"You've invited {totalInvites} member(s) to the server!"
        invitesEmbed = discord.Embed(title=invitesmessage, color=LIGHTPINK, timestamp=datetime.utcnow())

        vip = discord.utils.get(axolotlclan.roles, id=796851771510095882)  # accesses the role vip, and adds it to the user
        if totalInvites >= 3 and vip not in ctx.author.roles:
            viprank = str("congrats, you earned the VIP role!")
            vipembed = discord.Embed(title=viprank, color=LIGHTPINK)  # vip embed once they reach level 25
            await ctx.send(embed=vipembed)

            await ctx.author.add_roles(vip)

        await ctx.send(embed=invitesEmbed)
        
        
    @balls.error
    async def balls_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(error)
        else:
            print(error)
