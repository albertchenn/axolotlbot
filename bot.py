import os
import json     #python imports
import random

import discord
from dotenv import load_dotenv  #discord imports
from discord.ext import commands

with open('levels.json', 'r') as f:
    levels = json.load(f)           #takes the json file and makes it a "levels" dictionary

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #taking environment variables from .env
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = "$") #creates bot instance

@bot.event
async def on_ready():
    print('{} is on'.format(bot.user.name))                                   #gives notification when bot is online and sets game message to "Playing with Axolotls"
    await bot.change_presence(activity=discord.Game(name='with Axolotls'))

@bot.event
async def on_message(message):
    mutedchat = bot.get_channel(766656875256741898)
    spam = bot.get_channel(768876717422936115)
    music = bot.get_channel(757970344496726025) #channel declarations
    gulag = bot.get_channel(788434232401461248)               
    joinrole = bot.get_channel(765560283116208158)

    axolotl = bot.get_user(791048344956043274)
    rythm = bot.get_user(235088799074484224) #user declarations
    dyno = bot.get_user(155149108183695360)

    bannedchannels = [mutedchat, spam, music, gulag, joinrole]
    bannedusers = [axolotl, rythm, dyno]                #makes lists of blacklisted users

    if message.author == bannedusers:
        return          #doesn't do anything if a banned user(bot) speaks

    if not message.content:
        return          #doesn't do anything if no message is send; may change later

    if message.content.strip().lower() == "axolotl bot is bad": #triggers on the message "axolotl bot is bad"
        await message.author.create_dm()      #starts a "channel" which is actually just a dm
        await message.author.dm_channel.send("buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL")
        await message.author.dm_channel.send(file=discord.File('buffaxolotl.png')) #threatening dm

    if message.content.strip().lower() == "school sucks": #triggers on the message "school sucks"
        authorid = str(message.author.id) #finds the person's id
        authorping = '<@' + authorid + '>' #creates a ping message
        
        msgs = [] #creates empty list to log the pings
        await message.author.create_dm() #starts a dm channel
        for _ in range(5): #iterate 5 times
            sent_message = await message.author.dm_channel.send(authorping) #ping the person in dm channel
            msgs.append(sent_message) #log the message
        
        for message in msgs: #iterate through all the sent messages
            await message.delete() #delete them ;)

    if message.channel not in bannedchannels and message.content[0] != "." and message.content[0] != "?" and message.content[0] != "!": #check if it's not a spam channel or a bot command
        if str(message.author.id) not in levels: #if a new user joins and says something, create a new dictionary in the json file 
            levels[str(message.author.id)] = {"xp": 1, "level": 1} 
            print('new user') #debugging

        else:
            if 100 * (levels[str(message.author.id)]["level"] - 1) + 50 <= levels[str(message.author.id)]["xp"] + 1: #check if it passed the level; level cap is calculated as 100 * (level - 1) + 50
                levels[str(message.author.id)]["level"] += 1 #increase level by one
                levels[str(message.author.id)]["xp"] = 0 #reset xp
                levelUP = str(message.author.name) + " leveled up to " + str(levels[str(message.author.id)]["level"]) + "!" #create level up message
                levelupembed = discord.Embed(title = levelUP, color = 0xFFC0CB) #create embed with level up message
                await message.channel.send(embed = levelupembed) #send embed; YOU HAVE TO SEND THE EMBED FOR IT TO REGISTER

            else:   #any message sent
                added_xp = random.randint(1, 5) #xp randomized from 1-5, may change later
                levels[str(message.author.id)]["xp"] += added_xp #increase the xp by the randomized xp
        with open('levels.json', 'w') as f:
            f.write(json.dumps(levels, indent=4, sort_keys=True)) #save the dictionary of dictionaries of levels and xp to "levels.json"
        f.close()

    if message.content == ".level" or message.content == ".lvl": #triggers when ".level" or ".lvl" is sent
        if message.channel == spam: #only sends in spam and commands
            level = "level: " + str(levels[str(message.author.id)]["level"]) + "\n" #accesses the level of the person who sent it from the json file.   
            msgs = "xp: " + str(levels[str(message.author.id)]["xp"]) + "/" + str(100 * (levels[str(message.author.id)]["level"] - 1) + 50) #accesses the xp needed from the json file, (current xp/needed xp)
            
            levelinfoembed = discord.Embed(title = level + msgs, color = 0xff85a2) #creates embed of levels

            await message.channel.send(embed = levelinfoembed) #sends embed

@bot.event
async def on_member_join(member): #triggers on member join
    await member.create_dm() #creates dm channel
    await member.dm_channel.send(f"Hi, {member.name}, welcome to Axolotl Clan!\nMake sure to look at the <#763387839522013194> and <#758025770181460015>\nUse the join role channel to get your class or game roles!") #welcome and informational message

bot.run(TOKEN) #runs the program