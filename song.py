# python imports
import asyncio
from datetime import datetime
import os

# discord imports
import discord
from discord import embeds
from discord.ext import commands

# youtubedl
from youtube_dl import YoutubeDL

class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.np = {}
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist':'True',
            'outtmpl': 'songs/song.mp3',
            'quiet': 'True',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def downloadsearch(self, arg):
        with YoutubeDL(self.ydl_opts) as ydl:
            video = ydl.extract_info(f"ytsearch:{arg}", download=True)["entries"][0]

            return video

    def downloadlink(self, arg):
        with YoutubeDL(self.ydl_opts) as ydl:
            video = ydl.extract_info(arg, download=True)

        return video


    @commands.command(aliases=['play', 'p'], help="plays an mp3 song, do .playsong for more info")
    # @commands.has_role('VIP')
    async def _play(self, ctx, *, song):
        user = ctx.author

        if user.voice is None:
            await ctx.send("please join a vc before using this command")
            return
            
        vc = user.voice.channel
            
        if vc is not None:
            voice_channel = await vc.connect()
            channel = vc.name
            await ctx.send(user.name + " is in " + channel)
            await ctx.send("do '.stop' to stop the song, (you have to make it leave for it to play another song)")
            
            if os.path.exists("songs/song.mp3"):
                os.remove("songs/song.mp3")
            
            async with ctx.typing():
                songdata = self.downloadsearch(song)
            
            title = songdata["title"]
            url = songdata["webpage_url"]
            
            audio = discord.FFmpegPCMAudio('songs/song.mp3')
            
            voice_channel.play(audio)
            
            await ctx.send(f"Now playing: `{title}` from `{url}`")

            
        else:
            await ctx.send('User is not in a channel')


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
            
        else:
            npembed=discord.Embed(title="There is not a song currently playing", color=0xff58a2)
        
        await ctx.send(embed = npembed)