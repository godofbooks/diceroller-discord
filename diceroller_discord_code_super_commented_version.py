#this code was developed by godofbooks (https://github.com/godofbooks) as a personal project
#a very simple dice roller bot for discord. programmed in python 3.7. open source. 
#feel free to use and modify the code as you'd like. credit is appreciated. 

#resources used: 
#https://realpython.com/how-to-make-a-discord-bot-python/
#https://discordpy.readthedocs.io/en/latest/index.html

#this is the super commented version! intended for people just learning python or who want a more in-depth look at how and why this was programmed
#IDE used: Visual Studio 2019

#import packages
#os, random, and logging are natively part of python
import os
import random
import logging

#discord & dotenv have to be installed separately. the commands are above each package
#in Visual Studio 2019, click on Tools > Python > Python Environments. click the Overview dropdown, and select Packages (PyPl)
#pip install -U discord.py
import discord
#pip install -U python-dotenv
from dotenv import load_dotenv

#logging information; this outputs to the file discord.log each time the bot is started. this is not necessary for bot function, and can be deleted or commented out.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#gets info from drb.env
#this allows the bot token to be stored in a separate file, so it's not stored in plaintext in the code
load_dotenv("drb.env")
Token=os.getenv("DISCORD_TOKEN")
Guild=os.getenv("DISCORD_GUILD")

#establishes client variable
client = discord.Client()

#log in message
#this will print to the console when the bot is ready and waiting 
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

#establishes bot prefix
#by changing this, all commands will use this as the prefix to call the bot. default is $
bot_prefix="$"

#bot responses
#this block includes all functions for rolling dice, as well as the help and info commands.
@client.event
async def on_message(message):
    #this prevents the bot from responding to itself
    if message.author == client.user:
        return

    #list of DRS variables; these variables are accessed outside of the function DRS
    #DRS.nickname
    #DRS.Rolls_Total
    #DRS.sumRT
    #DRS.Modplus_int
    #DRS.Modplus_sum
    #DRS.Modminus_int
    #DRS.Modminus_sum
    #DRS.final_sum

    #$roll function- accepts all dice rolls formatted as ydx and all modifiers as +z or -z
    def DRS():
        if message.content.startswith('{0}roll'.format(bot_prefix)):
            DRS.nickname=message.author.display_name
            #takes message text, strips away $multi and whitespace, replaces - with +- for easier splitting, and splits text
            text=message.content
            strip_text=text.strip("{0}roll ".format(bot_prefix))
            strip_replace_text=strip_text.replace("-","+-")
            final_text=strip_replace_text.split("+")
            #$roll 3d4 +5 -2 +2d6 +4 -3 becomes 3d4 5 -2 2d6 4 -3

            #define lists
            Dice_Rolls=[]
            Modifiers=[]

            #check if 'd' appears in any list elements, if it does sort into list Dice_Rolls, otherwise sort into list Modifiers
            for d in final_text:
                if ("d" in d):
                    Dice_Rolls.append(d)
                else:
                    Modifiers.append(d)
            #3d4 +5 -2 +2d6 +4 -3 becomes 2 lists: Dice_Rolls:[3d4,2d6] and Modifiers:[5,-2,4,-3]
     
            #define variables
            DRlength=len(Dice_Rolls)
            rep=0
            DRS.Rolls_Total=[]

            #split Dice_Rolls into sub lists with structure [[y][x]]
            Dice_Rolls_split=[i.split("d",1) for i in Dice_Rolls]
            #Dice_Rolls becomes [[3][4],[2][6]]

            #while loop to roll [y] dice of [x] sides
            while rep < DRlength:
                rep2=0
                start=int(Dice_Rolls_split[rep][0])
                while rep2 < start:
                    rep2=rep2+1
                    num2=int(Dice_Rolls_split[rep][1])
                    roll=random.randint(1,num2)
                    DRS.Rolls_Total.append(roll)
                rep=rep+1
            DRS.sumRT=sum(DRS.Rolls_Total)

            #create 2 new lists, Modminus and Modplus
            Modminus=[]
            Modplus=[]

            #check if a '-' appears in any list elements of Modifiers, if it does sort into list Modminus, if it doesn't sort into list Modplus
            for minus in Modifiers:
                if ("-" in minus):
                    Modminus.append(minus)
                else:
                    Modplus.append(minus)
            #Modifiers becomes two lists: Modminus:[-2,-3] and Modplus[5,4]

            #sum Modplus
            DRS.Modplus_int=list(map(int,Modplus))
            DRS.Modplus_sum=sum(DRS.Modplus_int)
            #sums all the numbers in Modplus

            #sum Modminus, and multiply by -1 to get a negative value
            DRS.Modminus_int=list(map(int,Modminus))
            DRS.Modminus_sum=sum(DRS.Modminus_int)
            #sums all the numbers in Modminus

            #sum all lists together to get final answer
            DRS.final_sum=DRS.sumRT+DRS.Modplus_sum+DRS.Modminus_sum


    #list of Simple_DR variables; these variables are accessed outside of the function Simple_DR
    #Simple_DR.nickname
    #Simple_DR.final_roll
    #Simple_DR.message
    
    #$d function- this makes it easy to roll one dice quickly
    def Simple_DR():
        if message.content.startswith("{0}d".format(bot_prefix)):
            Simple_DR.nickname=message.author.display_name
            #takes the 2nd index (3rd character) and onward of the message, which should be the number of sides of the dice to be rolled
            dice_sides=message.content[2:]
            #sets dice_sides to be an integer for the roll variable below
            dice_sides_int=int(dice_sides)
            #selects a random integer between 1 and dice_sides_int
            roll=random.randint(1,dice_sides_int)
            #sets Simple_DR.final_roll to the string of roll; necessary for messages
            #if someone rolls a d20, and gets a 20 or a 1 there's a bit of flavor text for them
            Simple_DR.final_roll=str(roll)
            if dice_sides == "20" and Simple_DR.final_roll == "20":
                Simple_DR.message="Congratulations! {0} rolled a {1}.".format(Simple_DR.nickname,Simple_DR.final_roll)
            elif dice_sides == "20" and Simple_DR.final_roll == "1":
                Simple_DR.message="That's rough buddy. {0} rolled a {1}.".format(Simple_DR.nickname,Simple_DR.final_roll)
            else:
                Simple_DR.message="{0} rolled a {1}.".format(Simple_DR.nickname,Simple_DR.final_roll)

   
    #error handling try/except statements, this prevents the bot from crashing when an error is thrown

    #$roll error handling
    if message.content.startswith("{0}roll".format(bot_prefix)):
        try:
            DRS()
            await message.channel.send("{0} rolled a {1}.".format(DRS.nickname,DRS.final_sum))
            await message.channel.send("Dice Rolls: {0}, Positive Modifiers: {1}, Negative Modifiers: {2}.".format(DRS.sumRT,DRS.Modplus_sum,DRS.Modminus_sum))
            await message.channel.send("Rolls:{0}, Positive Modifiers:{1}, Negative Modifiers:{2}".format(DRS.Rolls_Total,DRS.Modplus_int,DRS.Modminus_int))
            print(message.author,"rolled a total of",DRS.final_sum,"with Dice Rolls totaling",DRS.sumRT,"and modifiers totaling",DRS.Modminus_sum+DRS.Modplus_sum)
        except Exception as error:
            await message.channel.send("Sorry, there was an error. Make sure you're typing the rolls right! If you need help, type $help")
            print("{0} caused an error: {1}".format(message.author,error))

    #$d error handling
    if message.content.startswith("{0}d".format(bot_prefix)):
        try:
            Simple_DR()
            await message.channel.send(Simple_DR.message)
            print(message.author,"rolled a {0}.".format(Simple_DR.final_roll))
        except Exception as error:
             await message.channel.send("Sorry, there was an error. Make sure you're typing the rolls right! If you need help, type $help")
             print("{0} caused an error: {1}".format(message.author,error))

    #$help
    if message.content.startswith("{0}help".format(bot_prefix)):
        await message.channel.send("**List of current commands:**\n"
            "\n"
            "*{0}info*\n"
            "Lists the prefix, bot developer, and coding information.\n"
            "\n"
            "*{0}help*\n"
            "Displays the commands list.\n"
            "\n"
            "*{0}dx*\n"
            "Rolls 1 die with x sides. No modifiers are allowed in this command.\n"
            "Correct useage: {0}d20     {0}d12\n"
            "Incorrect useage: {0}1d20     {0}d4 +5"
            "\n"
            "*{0}roll ydx +z:*\n"
            "Rolls y dice with x sides, with +z being modifiers and/or other dice.\n"
            "Correct useage: {0}roll 1d20     {0}roll 3d4 +5 +2d6 -2 \n"
            "Incorrect useage: {0}roll d20     {0}roll 3d4, +5, +2d6, -5     {0}roll 3d4 2d6\n"
            .format(bot_prefix))
        print(message.author,"requested the commands list")

    #$info
    if message.content.startswith("{0}info".format(bot_prefix)):
        await message.channel.send("**Bot Info**\n"
            "\n"
            "*Prefix*\n"
            "{0}\n"
            "\n"
            "*Bot Developer*\n"
            "godofbooks (https://github.com/godofbooks)\n"
            "\n"
            "*Programming and useage*\n"
            "Programmed in Python 3.7. Open source. Code available at https://github.com/godofbooks/diceroller-discord. \n"
            "\n"
            .format(bot_prefix))
        print(message.author,"requested the info list")

#runs the bot
client.run(Token)
