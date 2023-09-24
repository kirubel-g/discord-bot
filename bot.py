from discord.ext import commands, tasks
import discord
from dataclasses import dataclass #for study timer
import datetime

BOT_TOKEN = 'MTE1NTM3MjY0OTQ2MDAyMzM2Nw.GmI_KP.zh2lajfR3Ci5XWBCQF2AJF-DrcCID8hDzmi4j0'
#I know best practice is to not give out your token, but I thought this hackathon warranted an exception
CHANNEL_ID = 1155380168169369701
MAX_SESSION_TIMES = 30

@dataclass #defining a class
class Session:
    is_active: bool = False #defining methods
    start_time: int = 0

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #client connection to Discord, how we communicate with Discord
#I'm  using bot command instead of commands.Client b/c the bot one has more helper functions I wanna use
session = Session()

#handler is a function that runs on certain event triggers
@bot.event
async def on_ready(): #on ready is essentially what the code runs when I open up/login to Discord
    print('Hello! Study bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Hello! Study bot is ready!') #asynchronous function, so it needs await in front of it
    # 'await' makes the function wait for this line to finish running before proceeding to the next line

@bot.command() #name of function becomes name of command for use later
async def hello(ctx): #all commands have context as first argument, gives us info on how command is sent to bot
    await ctx.send('Hello!')

# @bot.command()
# async def add(ctx, *arr): # *arr will take an unlimited amount of inputs and assume they are arrays
#     result = 0
#     for i in arr:
#         result += int(i)
#     await ctx.send(f"Result: {result}")

@tasks.loop(minutes=MAX_SESSION_TIMES, count=2)
async def break_reminder():
    #we don't want the warning to happen immediately, so ignore the first iteration
    if break_reminder.current_loop == 0:
        return
    channel = bpt.get_channel(CHANNEL_ID)
    await channel.send(f"Take a break! You've been studying for 30 minutes.")

@bot.command()
async def start(ctx):
    #if session has started already, return a reminder that it is 
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True 
    session.start_time = ctx.message.created_at.timestamp()
    readable_time = ctx.message.created_at.strftime("%H:%H:%S") #create a message at time of command
    await ctx.send(f"Session started at {readable_time}") #send above message

@bot.command()
async def end(ctx):
    #edge case
    if not session.is_active:
        await ctx.send('No session is active!')
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time #in seconds, see if you can't make it better
    human_readable_duration = str(datetime.timedelta(seconds=duration)) #make data readable
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}.")

bot.run(BOT_TOKEN)