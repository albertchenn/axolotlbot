import os
import json

import discord
from dotenv import load_dotenv
from discord.ext import commands

with open('levels.json', 'r') as f:
    levels = json.load(f)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = "$")

@bot.event
async def on_ready():
    print('{} is on'.format(bot.user.name))
    await bot.change_presence(activity=discord.Game(name='with axolotls'))

@bot.event
async def on_message(message):
    mutedchat = bot.get_channel(766656875256741898)
    spam = bot.get_channel(768876717422936115)
    music = bot.get_channel(757970344496726025)
    gulag = bot.get_channel(788434232401461248)
    joinrole = bot.get_channel(765560283116208158)

    axolotl = bot.get_user(791048344956043274)
    rythm = bot.get_user(235088799074484224)
    dyno = bot.get_user(155149108183695360)

    bannedchannels = [mutedchat, spam, music, gulag, joinrole]
    bannedusers = [axolotl, rythm, dyno]

    if message.author == bannedusers:
        return
    if not message.content:
        return
    if message.content.strip().lower() == "axolotl bot is bad":
        await message.author.create_dm()
        await message.author.dm_channel.send("buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL")
        await message.author.dm_channel.send(file=discord.File('buffaxolotl.png'))
    if message.content.strip().lower() == "school sucks":
        authorid = str(str(message.author.id))
        authorping = '<@' + authorid + '>'
        
        msgs = []
        await message.author.create_dm()
        for _ in range(5):
            sent_message = await message.author.dm_channel.send(authorping)
            msgs.append(sent_message)
        
        for message in msgs:
            await message.delete()
    if message.content.strip().lower() == "test":
        await message.channel.send("hello there, " + '<@' + str(message.author.id) + '>')

    if message.channel not in bannedchannels and message.content[0] != "." and message.content[0] != "?" and message.content[0] != "!":
        if str(message.author.id) not in levels:
            levels[str(message.author.id)] = {"msgs": 1, "level": 1}
            print('new user')
        else:
            if 100 * (levels[str(message.author.id)]["level"] - 1) + 50 == levels[str(message.author.id)]["msgs"] + 1:
                levels[str(message.author.id)]["level"] += 1
                levels[str(message.author.id)]["msgs"] = 0
                levelUP = str(message.author.name) + " leveled up to " + str(levels[str(message.author.id)]["level"]) + "!"
                levelupembed = discord.Embed(title = levelUP, color = 0xFFC0CB)
                await message.channel.send(embed = levelupembed)
            else:
                levels[str(message.author.id)]["msgs"] += 1
        with open('levels.json', 'w') as f:
            f.write(json.dumps(levels, indent=4, sort_keys=True)) 
        f.close()
    if message.content == ".level" or message.content == ".lvl":
        if message.channel == spam:
            level = "level: " + str(levels[str(message.author.id)]["level"]) + "\n"   
            msgs = "msgs since last level up: " + str(levels[str(message.author.id)]["msgs"])
            
            levelinfoembed = discord.Embed(title = level + msgs, color = 0xff85a2)

            await message.channel.send(embed = levelinfoembed)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi, {member.name}, welcome to Axolotl Clan!\nMake sure to look at the <#763387839522013194> and <#758025770181460015>\nUse the join role channel to get your class or game roles!")

bot.run(TOKEN)