# python imports
import asyncio
from datetime import datetime
import os

# discord imports
import discord
from discord import embeds
from discord.ext import commands

# youtubedl
import youtube_dl

class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.np = {}

    @commands.command(aliases=['play', 'p'], help="plays an mp3 song, do .playsong for more info")
    @commands.has_role('VIP')
    async def _play(self, ctx, *args):
        user = ctx.author
        
        songs = ["pog", "pogU", "Wait", "what", "manhunt", "bestsong", "men", "pathetique", "arabesque", "youtube"]
        if user.voice is None:
            await ctx.send("please join a vc before using this command")
            return
            
        vc = user.voice.channel
        
        if len(args) == 0:
            await ctx.send('the songs that are currently available are: ' + str(songs))
            return
            
        elif args[0] in songs:
            self.np["song"] = args[0]
            
            if vc is not None:
                voice_channel = await vc.connect()
                channel = vc.name
                await ctx.send(user.name + " is in " + channel)
                await ctx.send("do '.stop' to stop the song, (you have to make it leave for it to play another song)")

                if len(args) == 1:
                    self.np["isloop"] = False
                    voice_channel.play(discord.FFmpegPCMAudio("songs/" + args[0] + ".mp3"))
                    self.np["currentTime"] = 0
                    
                    while voice_channel.is_playing():
                        await asyncio.sleep(1)
                        self.np["currentTime"] += 1

                elif args[1] == "loop":
                    self.np["isloop"] = True
                    await ctx.send("you have chosen the 'loop' switch, it will play endlessly unless you stop it.")
                    while True:
                        voice_channel.play(discord.FFmpegPCMAudio("songs/" + args[0] + ".mp3"))
                        self.np["currentTime"] = 0
                        
                        while voice_channel.is_playing():
                            self.np["currentTime"] += 1
                            await asyncio.sleep(1)
                            
                voice_channel.stop()
            else:
                await ctx.send('User is not in a channel')

        elif args[0] == "all":
            self.np["song"] = args[0]
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


    @commands.command(name='stop', help='leaves the vc')
    async def _stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        
        if voice_client is not None:
            await voice_client.disconnect()
            await ctx.send("axolotl has left the vc")
            self.np = {}
            
        else:
            await ctx.send('axolotl is not in a channel')
    
    @commands.command(name='np', help='displays current playing song (if any)')
    async def _np(self, ctx):
        if self.np != {}: 
            npembed=discord.Embed(title="Song Info", description="current song info", color=0xff85a2)
            npembed.add_field(name="Song", value=self.np["song"], inline=True)
            npembed.add_field(name="Loop", value=self.np["isloop"], inline=True)
            
            curinsec = self.np["currentTime"]
            
            endseconds = str(curinsec - curinsec // 60 * 5)
            endseconds = endseconds.rjust(2, "0")
            
            curinmin = f"{curinsec // 60}:{endseconds}"
            
            
            npembed.add_field(name="time elapsed", value=curinmin)
        else:
            npembed=discord.Embed(title="There is not a song currently playing", color=0xff58a2)
        
        await ctx.send(embed = npembed)