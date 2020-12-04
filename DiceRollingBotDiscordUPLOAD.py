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

    #dice rolling
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #$roll function
    if message.content.startswith('$roll'):
        nickname=message.author.display_name
        #takes message text, strips away $multi and whitespace, replaces - with +- for easier splitting, and splits text
        text=message.content
        strip_text=text.strip("$roll ")
        strip_replace_text=strip_text.replace("-","+-")
        final_text=strip_replace_text.split("+")

        #define lists
        Dice_Rolls=[]
        Modifiers=[]

        #check if 'd' appears in any list elements, if it does sort into list Dice_Rolls, otherwise sort into list Modifiers
        for d in final_text:
            if ("d" in d):
                Dice_Rolls.append(d)
            else:
                Modifiers.append(d)
     
        #define variables
        DRlength=len(Dice_Rolls)
        rep=0
        Rolls_Total=[]

        #split Dice_Rolls into sub lists with structure [[y][x]]
        Dice_Rolls_split=[i.split("d",1) for i in Dice_Rolls]

        #while loop to roll [y] dice of [x] sides for all occurances in Dice_Rolls_Split
        while rep < DRlength:
            rep2=0
            start=int(Dice_Rolls_split[rep][0])
            while rep2 < start:
                rep2=rep2+1
                num2=int(Dice_Rolls_split[rep][1])
                roll=random.randint(1,num2)
                Rolls_Total.append(roll)
            rep=rep+1
        sumRT=sum(Rolls_Total)

        #create 2 new lists, Modminus and Modplus
        Modminus=[]
        Modplus=[]

        #check if a '-' appears in any list elements of Modifiers, if it does sort into list Modminus, if it doesn't sort into list Modplus
        for minus in Modifiers:
            if ("-" in minus):
                Modminus.append(minus)
            else:
                Modplus.append(minus)

        #sum Modplus
        Modplus_int=list(map(int,Modplus))
        Modplus_sum=sum(Modplus_int)

        #sum Modminus
        Modminus_int=list(map(int,Modminus))
        Modminus_sum=sum(Modminus_int)

        #sum all lists together to get final answer
        final_sum=sumRT+Modplus_sum+Modminus_sum

        #send messages to channel
        await message.channel.send("{0} rolled a {1}.".format(nickname,final_sum))
        await message.channel.send("Dice Rolls: {0}, Positive Modifiers: {1}, Negative Modifiers: {2}.".format(sumRT,Modplus_sum,Modminus_sum))
        
        #print messages to console
        print(nickname,message.author,"rolled a total of",final_sum,"with Dice Rolls totaling",sumRT,"and modifiers totaling",Modminus_sum+Modplus_sum)

    #$commands
    if message.content.startswith("$commands"):
        await message.channel.send("**List of current commands:**\n"
            "**$info**\n"
            "Lists the prefix, bot developer, and coding information.\n"
            "\n"
            "**$roll ydx +z:**\n"
            "Rolls y dice with x sides and z modifiers. As many types of dice as necessary with any modifiers necessary can be rolled at once.\n"
            )
        print(nickname,message.author,"requested the commands list")

    #$info
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
        print(nickname,message.author,"requested the info list")

#runs the bot
client.run(Token)
