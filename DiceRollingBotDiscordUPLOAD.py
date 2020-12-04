#this code was developed by godofbooks (https://github.com/godofbooks) as a personal project
#a very simple dice roller bot for discord. programmed in python 3.7. open source. 
#feel free to use and modify the code as you'd like. credit is appreciated. 

#resources used: 
#https://realpython.com/how-to-make-a-discord-bot-python/
#https://discordpy.readthedocs.io/en/latest/index.html

#import packages
import os
import random
#pip install -U discord.py
import discord
#pip install -U python-dotenv
from dotenv import load_dotenv

#gets info from drb.env
load_dotenv("drb.env")
Token=os.getenv("DISCORD_TOKEN")
Guild=os.getenv("DISCORD_GUILD")

#establishes client & nickname
client = discord.Client()

#log in message 
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

    for guild in client.guilds:
        if guild.name == Guild:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

#dice rolling
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #$dx; replace x with any number
    if message.content.startswith('$d'):
        #defines nickname to be the user's display name in the server
        nickname=message.author.display_name
        #sets x equal to the 2nd index, should be equivalent to x
        x=message.content[2:]
        #makes x an integer
        x2=int(x)
        #rolls a random number between 1 and x2
        roll=random.randint(1,x2)
        #reformats roll to a string
        rolls=str(roll)
        #prints result to console
        print(nickname,"rolled a d",x,"and got",rolls)
        #if someone rolls a d20 using this command and gets a 20 or a 1 there's a bit of flavor text
        if message.content == "$d20":
            if rolls == "1":  
                await message.channel.send("That's rough buddy. {0} rolled a {1}.".format(nickname,rolls))
            elif rolls == "20":
                await message.channel.send("Congratulations! {0} rolled a {1}.".format(nickname,rolls))
            else:
                await message.channel.send("{0} rolled a {1}.".format(nickname,rolls))
        #sends result to channel: "(nickname) rolled a (total)"
        else:
            await message.channel.send("{0} rolled a {1}.".format(nickname,rolls))


    #$multi ydx; roll y of x-sided dice
    if message.content.startswith('$multi'):
        #defines nickname to be the user's display name in the server
        nickname=message.author.display_name
        #sets y equal to the 7th index, should be equivalent to y
        y=message.content[7]
        #makes y an integer
        y2=int(y)
        #sets x equal to the 9th index, should be equivalent to x
        x=message.content[9:]
        #makes x an integer
        x2=int(x)
        #sets k to 1 for the count on the while loop
        k=1
        #creates C as an empty list
        C=[]
        #rolls y random numbers, and appends them to C
        while k <= y2:
            k=k+1
            roll=random.randint(1,x2)
            C.append(roll)
        #sums up all values in C
        t=sum(C)
        #reformats roll to a string
        rolls=str(t)
        #prints result to console
        print(nickname,"rolled",y,"d",x,"and got",rolls, C)
        #sends results to channel, including what each individual roll was
        await message.channel.send("{0} rolled a {1}.".format(nickname,rolls))
        await message.channel.send(C)
    
    #$commands
    #lists all available commands 
    if message.content.startswith("$commands"):
        await message.channel.send("**List of current commands:**\n"
            "**$info**\n"
            "Lists the prefix, bot developer, and coding information.\n"
            "\n"
            "**$dx:**\n"
            "Rolls 1 die with x sides.\n"
            "\n"
            "**$multi ydx:**\n"
            "Rolls y dice with x sides.\n"
            )
        #prints result to console
        print(nickname,message.author,"requested the commands list")

    #$info
    #information about bot
    if message.content.startswith("$info"):
        await message.channel.send("**Bot Info**\n"
            "\n"
            "**Prefix**\n"
            "$\n"
            "\n"
            "**Bot Developer**\n"
            "godofbooks (https://github.com/godofbooks)\n"
            "\n"
            "**Programming and useage**\n"
            "Programmed in Python 3.7. Open source. Code available at https://github.com/godofbooks/diceroller-discord. \n"
            "\n"
            )
        #prints result to console
        print(nickname,message.author,"requested the info list")

#runs the bot
client.run(Token)
