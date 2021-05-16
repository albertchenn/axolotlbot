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

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = YoutubeDL(ydl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('webpage_url')
        self.uploader = data.get('uploader')
        
    @classmethod
    async def from_song(cls, song, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{song}", download=False))

        if 'entries' in data:

            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Song(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.np = {}

    @commands.command()
    async def join(self, ctx):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        
    @commands.command(aliases=["p"], help="play song lmao")
    async def play(self, ctx, *, song):

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        
        async with ctx.typing():
            player = await YTDLSource.from_song(song, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: `{player.title}` by `{player.uploader}` from `{player.url}`')
    
            
    @commands.command(name='stop', help='leaves the vc')
    async def _stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        
        if voice_client is not None:
            await voice_client.disconnect()
            await ctx.send("axolotl has left the vc")
            self.np = {}
            
        else:
            await ctx.send('axolotl is not in a channel')
    
    @commands.command(name='volume', help='changes volume')
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("User is not in a channel")
        
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}")
        
    @commands.command(name='np', help='displays current playing song (if any)')
    async def _np(self, ctx):
        if self.np != {}: 
            npembed=discord.Embed(title="Song Info", description="current song info", color=0xff85a2)
            npembed.add_field(name="Song", value=self.np["song"], inline=True)
            npembed.add_field(name="Requested by", value=self.np["requested"], inline=True)
        else:
            npembed=discord.Embed(title="There is not a song currently playing", color=0xff58a2)
        
        await ctx.send(embed = npembed) # FIXME: add like everything
    
    # TODO: ADD LOOP
    # TODO: ADD ERROR MESSAGE IF BOT IS CURRENTLY PLAYING SONG