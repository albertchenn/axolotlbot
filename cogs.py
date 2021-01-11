#cogs.py
import os
import json     #python imports
import random
from datetime import datetime
import time

import discord
from discord import player
from dotenv import load_dotenv  #discord imports
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.play_again = "yes"
        self.ladders = {          # these two dictionaries are for the snakes and ladders game, and the third is for the trivia game.
            3: 37,
            6: 16,
            14: 32,
            27: 56,
            41: 85,
            69: 87,
            79: 98,
            89: 91
        }
        self.snakes = {
            15: 9,
            42: 17,
            49: 12,
            58: 45,
            61: 22,
            75: 47,
            88: 36,
            94: 64,
            97: 65
        }

    
    def playermove(self):           # the playermove function is a function that rolls the dice for the snakes and ladders game
        x = random.randint(1,6)
        return x
   
    @commands.command()
    async def play(self, ctx):
        while self.play_again.lower() == "yes":
            message = "Welcome to the main menu! We have three games to choose from!"
            messageEmbed = discord.Embed(title = message)
            await ctx.send(embed = messageEmbed)
            gameMessage = "Would you like to play rock-paper-scissors, a guessing game, snakes and ladders, or a trivia game? Enter snakes + ladders - 1, guessing game - 2, rock paper scissors - 3. "
            gameEmbed = discord.Embed(title = "Make ur decision", description = gameMessage)
            await ctx.send(embed = gameEmbed)
            
            msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content == "1":        # make an if statement to determine which game the player wants to play
                await ctx.send('Welcome to Snakes and Ladders! You will be playing against a computer. To continue, type "roll", and you will roll a die see what square you land on. If you hit a ladder, you will go to a higher square. If you hit a snake, you will go to a lower square.  The first player to reach square 100 wins!')
                replay = "yes"
                while replay.lower() == "yes":            # while loop for replayability
                    scr = 0
                    ai = 0
                    while scr < 100 and ai < 100:     # make a while loop for the player until they reach square 100 or more
                        time.sleep(0.5)
                        await ctx.send('\ntype "roll" to roll the dice. ')
                        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                        if msg.content.lower() == "roll":
                            roll = self.playermove()
                            scr += roll
                            time.sleep(0.5)
                            await ctx.send('\nYou are at square ' + str(scr))
                            roll = self.playermove()
                            ai += roll
                            time.sleep(0.5)
                            await ctx.send('Computer is at square ' + str(ai))
                        else: 
                            await ctx.send('bad input, try again')
                        if scr in self.snakes:           # dictionaries are used for the snakes and ladders here
                            time.sleep(0.5)
                            await ctx.send("\nYou caught a snake from square " + str(scr) + " to square " + str(self.snakes.get(scr)))
                            scr = self.snakes.get(scr)
                        elif scr in self.ladders:
                            time.sleep(0.5)
                            await ctx.send("\nYou got a ladder from square " + str(scr) + " to sqaure " + str(self.ladders.get(scr)))
                            scr = self.ladders.get(scr)
                        if ai in self.snakes:
                            time.sleep(0.5)
                            await ctx.send("\nComputer caught a snake from square " + str(ai) + " to square " + str(self.snakes.get(ai)))
                            ai = self.snakes.get(ai)
                        elif ai in self.ladders:
                            time.sleep(0.5)
                            await ctx.send("\nComputer got a ladder from square " + str(ai) + " to square " + str(self.ladders.get(ai)))
                            ai = self.ladders.get(ai)
                    if scr >= 100:
                        await ctx.send('\nYou win!')
                    elif ai >= 100:
                        await ctx.send('\nComputer wins! Better luck next time!')
                    await ctx.send("\nWould you like to play this game again? (type 'yes' if you want to play again, or press anything else to exit.) ")
                    replay = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    replay = replay.content
            elif msg.content == "2":
                time.sleep(0.5)
                await ctx.send('Welcome to the Guessing Game! Players will guess a number from 1 to 1000. After guessing, the player will be told whether or not their choice was too high or low. Players also have 10 guesses to choose the random number.')
                replay = "yes"
                while replay.lower() == "yes":              # while loop for replayability
                    number = random.randint(1,1000)
                    guesses = 10
                    while guesses > 0:
                        try:   
                            time.sleep(0.5) 
                            await ctx.send("\nGuess a number from 1 to 1000: ")
                            guess = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                            guess = int(guess.content)
                            if guess == number:
                                time.sleep(0.5)
                                await ctx.send("\nYou guessed correctly, you won!")
                                break
                            elif guess > number:
                                guesses -= 1
                                time.sleep(0.5)
                                await ctx.send("\nYou guessed too high! You have " + str(guesses) + " guesses left.")
                            else:
                                guesses -= 1
                                time.sleep(0.5)
                                await ctx.send("\nYou guessed too low! You have " + str(guesses) + " guesses left.")
                        except:
                            time.sleep(0.5)
                            await ctx.send('Bad input, make sure you write an integer.')
                    if guesses == 0:
                        time.sleep(0.5)
                        await ctx.send("\nYou lost! The number was " + str(number)) 
                    
                    time.sleep(0.5)
                    await ctx.send("\nWould you like to play this game again? (type 'yes' if you want to play again, or press anything else to exit.) ")
                    replay = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    replay = replay.content
            elif msg.content == "3":
                time.sleep(0.5)
                await ctx.send('Welcome to Rock Paper Scissors! To play the game, type "rock" , "paper", or "scissors" when prompted to. Then, you will see what the computer chose and whether or not you won!')
                replay = "yes"
                while replay.lower() == "yes":     # while loop for replayability
                    bot_choice = random.randint(1,3)    #computer picks a random number which is rock, paper, or scissors
                    time.sleep(0.5)
                    await ctx.send("\nDo you pick rock (r), paper (p), or scissors (s)? ")
                    choice = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    choice = choice.content
                    if choice == "r":
                        if bot_choice == 1:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose rock, you tied!")
                        elif bot_choice == 2:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose paper, you lost!")
                        else:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose scissors, you won!")
                    elif choice == "s":
                        if bot_choice == 1:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose rock, you lost!")
                        elif bot_choice == 2:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose paper, you won!")
                        else:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose scissors, you tied!")
                    elif choice == "p":
                        if bot_choice == 1:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose rock, you won!")
                        elif bot_choice == 2:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose paper, you tied!")
                        else:
                            time.sleep(0.5)
                            await ctx.send("\nBot chose scissors, you lost!")
                    else:
                        time.sleep(0.5)
                        await ctx.send("bad input, make sure everything is lowercase")
                    await ctx.send("Would you like to play this game again? (type 'yes' if you want to play again, or type anything else to exit.) ")
                    replay = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    replay = replay.content
            else:
                continue

            await ctx.send("Would you like to play another game? Type yes or no. ")
            self.play_again = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
