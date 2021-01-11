#bot.py
import os
import json     #python imports
import random
from datetime import datetime
from cogs import Games

import discord
from dotenv import load_dotenv  #discord imports
from discord.ext import commands

with open('levels.json', 'r') as f:
    levels = json.load(f)           #takes the json file and makes it a "levels" dictionary
    
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #taking environment variables from .env

bot = commands.Bot(command_prefix = ".") #creates bot instance

@bot.event
async def on_ready():
    print('{} is on'.format(bot.user.name))                                   #gives notification when bot is online and sets game message to "Playing with Axolotls"
    await bot.change_presence(activity=discord.Game(name='with Axolotls'))

    roles = bot.get_channel(797867864593006592)

    
    reactionmessage = """:triangular_ruler: - precalc\n
                         :book: - ela (thompson)\n
                         :tools: - ied\n
                         :straight_ruler: - algebra 2\n
                         :earth_americas: - world history\n
                         :blue_square: - salem\n
                         :black_large_square: - plymouth\n
                         :red_square: - canton\n
                         :loudspeaker: - announcements\n
                         :man_scientist: - biology\n
                         :flag_fr: - french\n
                         :united_nations: - ap world\n
                         :closed_book: - ela (wright)\n
                         :detective: - gulag\n
                         :microphone2: - debate\n"""

    reactionembed = discord.Embed(title = "react to the following emojis for ur roles", description = reactionmessage)

    message = await roles.send(embed = reactionembed)
        
    emojis = ['📐', '📖', '🛠️', '📏', '🌎', '🟦', '⬛', '🟥', '📢', '👨‍🔬', '🇫🇷', '🇺🇳', '📕', '🕵️‍♂️', '🎙️']
    for emoji in emojis:
        await message.add_reaction(emoji)

    reactionmessage = """:computer: - cse\n
                        :robot: - robotics\n
                        :rocket: - physics (gell)\n
                        :airplane_departure: - physics (hiske)\n
                        :flag_es: - spanish 2\n
                        :flag_mx: - spanish 3\n
                        :heavy_division_sign: - math olympiad\n"""
    
    reactionembed = discord.Embed(description = reactionmessage)

    message = await roles.send(embed = reactionembed)

    emojis = ['💻', '🤖', '🚀', '🛫', '🇪🇸', '🇲🇽', '➗']    
    for emoji in emojis:
        await message.add_reaction(emoji)
    
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

    axolotlclan = bot.get_guild(591065297692262410) #guild declarations

    bannedchannels = [mutedchat, spam, music, gulag, joinrole]   #makes lists of blacklisted channels
    bannedusers = [axolotl, rythm, dyno]            #makes lists of blacklisted users

    if message.author == bannedusers:
        return          #doesn't do anything if a banned user(bot) speaks

    if not message.content:
        return          #doesn't do anything if no message is send; may change later

    if "axolotl bot is bad" in message.content.lower(): #triggers on the message "axolotl bot is bad"
        #await message.author.create_dm()      #starts a "channel" which is actually just a dm
        await message.author.send("buff axolotl is coming for you, so prepare yourself mortal.\nYou shall not stand the wrath of BUFF AXOLOTL")
        await message.author.send(file=discord.File('buffaxolotl.png')) #threatening dm

    if "school sucks" in message.content.lower(): #triggers on the message "school sucks"
        authorid = str(message.author.id) #finds the person's id
        authorping = '<@' + authorid + '>' #creates a ping message
        
        msgs = [] #creates empty list to log the pings
        for _ in range(5): #iterate 5 times
            sent_message = await message.author.send(authorping) #ping the person in dm channel
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

                if levels[str(message.author.id)]["level"] >= 10:
                    viprank = str("congrats, you earned the VIP role!")
                    vipembed = discord.Embed(title = viprank, color = 0xff85a2) #vip embed once they reach level 25
                    await message.channel.send(embed = vipembed)

                    vip = discord.utils.get(axolotlclan.roles, name = "VIP")  #accesses the role vip, and adds it to the user
                    await message.author.add_roles(vip)

            else:   #any message sent
                added_xp = random.randint(1, 5) #xp randomized from 1-5, may change later
                levels[str(message.author.id)]["xp"] += added_xp #increase the xp by the randomized xp
        with open('levels.json', 'w') as f:
            f.write(json.dumps(levels, indent=4, sort_keys=True)) #save the dictionary of dictionaries of levels and xp to "levels.json"
        f.close()

    await bot.process_commands(message)

@bot.event
async def on_member_join(member): #triggers on member join
    main = bot.get_channel(763475634278105088)

    await member.dm_channel.send(f"Hi, {member.name}, welcome to Axolotl Clan!\nMake sure to look at the <#763387839522013194> and <#758025770181460015>\nUse the join role channel to get your class or game roles!") #welcome and informational message
    await main.send(f"{member.name} is here!")

@bot.event
async def on_reaction_add(reaction, user):
    roles = bot.get_channel(797867864593006592)
    axolotl = bot.get_user(791048344956043274)
    axolotlclan = bot.get_guild(591065297692262410)

    emojiRoles = {'📐': 'Precalc', '📖': 'ELA (Thompson)', '🛠️': 'IED', '📏': 'Algebra 2', '🌎': 'World History',
                  '🟦': 'Salem', '⬛': 'Plymouth', '🟥': 'Canton', '📢': 'Announcements', '👨‍🔬': 'Biology', '🇫🇷': 'French', 
                  '🇺🇳': 'AP World', '📕': 'ELA (Wright)', '🕵️‍♂️': 'Gulag', '🎙️': 'Debate', '💻': 'CSE', '🤖': 'Robotics', 
                  '🚀': 'Physics (Gell)', '🛫': 'Physics (Hiske)', '🇪🇸': 'Spanish 2', '🇲🇽': 'Spanish 3', '➗': 'Math Olympiad'}

    if reaction.message.channel != roles:
        return
    elif user == axolotl:
        return
    else:
        role = discord.utils.get(axolotlclan.roles, name = emojiRoles[str(reaction)])
        if role in user.roles:
            await user.remove_roles(role)
        else:
            await user.add_roles(role)
        await reaction.remove(user)

@bot.command(aliases=['lvl', 'level'])
async def _level(ctx):
    message = ctx.message
    
    level = "level: " + str(levels[str(message.author.id)]["level"]) + "\n" #accesses the level of the person who sent it from the json file.   
    msgs = "xp: " + str(levels[str(message.author.id)]["xp"]) + "/" + str(100 * (levels[str(message.author.id)]["level"] - 1) + 50) #accesses the xp needed from the json file, (current xp/needed xp)
    
    levelinfoembed = discord.Embed(title = level + msgs, color = 0xff85a2, timestamp=datetime.utcnow()) #creates embed of levels (and sets a timestamp)
    levelinfoembed.set_footer(text='Retrieved Data')

    await ctx.send(embed = levelinfoembed)


@bot.command(aliases=['invites'])
async def _invites(ctx):
    axolotlclan = bot.get_guild(591065297692262410)
    message = ctx.message

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    invitesmessage = f"You've invited {totalInvites} member(s) to the server!"
    invitesEmbed = discord.Embed(title = invitesmessage, color = 0xff85a2, timestamp=datetime.utcnow())
    
    if totalInvites >= 3:
        viprank = str("congrats, you earned the VIP role!")
        vipembed = discord.Embed(title = viprank, color = 0xff85a2) #vip embed once they reach level 25
        await message.channel.send(embed = vipembed)

        vip = discord.utils.get(axolotlclan.roles, name = "VIP")  #accesses the role vip, and adds it to the user
        await message.author.add_roles(vip)
        
    await ctx.send(embed = invitesEmbed)
    
bot.add_cog(Games(bot))
bot.run(TOKEN) #runs the program