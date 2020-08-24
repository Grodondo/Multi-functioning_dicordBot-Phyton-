import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions 
from discord.utils import get
from itertools import cycle
from datetime import datetime, timedelta
import random
import os
import sys
import traceback
import pw
import mysqlfunctions

#Made by Grodondo(Cdj), planning on updating it later on and including a monetary system.
#This was a project made for a discord server based on the Ping Pong minigame from Overwatch, feel free to change its code at will.


Prefix = "!"
client = commands.Bot(command_prefix = Prefix)
Client = discord.Client()
client.remove_command("help")

status = cycle(["Overwatch", "Overwatch Ping Pong"])

@client.event
async def on_ready():
    print("The bot is working")
    bot_status.start()
    #await client.change_presence(activity=discord.Activity(name="Overwatch Ping Pong", type=discord.ActivityType.playing))


@tasks.loop(seconds=5)
async def bot_status():
    await client.change_presence(activity=discord.Game(next(status)))

#---------------------COGS:----------------------
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command() 
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#-------------------------------------------------

@client.command(aliases=["Ping"])
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases=["rudolf,", "rudolf", "Rudolf,"])
async def Rudolf(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Dont think so, maybe?"
                "You are not as desesperate as to believe in a bot, right?",
                "Instead of asking me this, you could be doing something usefull..."] 
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

greet = ["hi", "hello", "hola", "salut", "greetings", "Hi", "Hello", "Hola", "Salut"]
@client.command(aliases=greet)
async def Greetings(message):
    #message.content = message.content.lower()
    responses = ["hope you day is now a litle better.",
                "the ball will show us the way.",
                "better be carefull, there are too many good players here.",
                "live well my friend.",
                "Hope we get along, or so said **cdj**",
                "may the power of the ball guide you."]
    #if message.content.startswith("hi", "hello", "hola", "salut", "greetings"):
    await message.send(f"Hello ** {message.author.name}**, {random.choice(responses)}")   

@client.command(aliases=["Placements", "placements"])
async def results(ctx):
    embed = discord.Embed(
        colour = discord.Color.green()
    )
    embed.set_author(name="Placements:")
    embed.add_field(name="1st Ping_Pogathon", value="1st_Place: ShadowStorm / 2nd_Place: Cdj / 3rd_Place: OhFeck / Most_Kills: Sof", inline=False)
    embed.add_field(name="2nd Ping_Pogathon", value="1st_Place: OhFeck / 2nd_Place: BLPHCineGame / 3rd_Place: Deltacor / Most_Kills: OhFeck", inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=["help"])  
async def Help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Color.orange()
    )

    embed.set_author(name="FUNCTIONS: ")
    embed.add_field(name="ping", value="returns the bots ping.", inline=False)
    embed.add_field(name="hi", value="Its a good conversation starter.", inline=False)
    embed.add_field(name="Rudolf", value="Ask him any question after its name, and he shall respond.", inline=False)
    embed.add_field(name="Play + {URL}", value="The bot will put on whatever video you choose.", inline=False)
    embed.add_field(name="Leave / Stop", value="Will order the Bot to leave the voice channel.", inline=False)
    embed.add_field(name="createPoll ¨question¨ arg arg arg...", value="Creates a Poll, takes from 2 to 10 arguments", inline=False)
    embed.add_field(name="Placements", value="Shows the winners of every Ping Pongathon tournament", inline=False)
    embed.add_field(name="addTournament", value='adds Tournament \n parameters:date , gamemap , gamnetype , speed, [comment]; \nif a parameter contains whitespaces soround it with "". Dates are noted as Day/Month/Year', inline=False)
    embed.add_field(name="register", value='adds a new User \n parameters: battletag , name , email , [nickname]; ', inline=False)
    embed.add_field(name="participate", value="lets you participate in the next tournament", inline=False)

    embed.set_footer(text="Prefix:  " + Prefix)

    await author.send(embed=embed)


#database commands:

@client.command( aliases=["addTournament"])
@has_permissions(manage_guild=True)
async def addTornament(ctx, date, gamemap, gametype, speed, comment="No Comment",):

    #await ctx.invoke(ctx.bot.get_command('ping'))
    #await ctx.invoke(ctx.bot.get_command('Poll'), hours=11, question="", options=['1pm'])
    await ctx.invoke(ctx.bot.get_command('Time_Poll'), 24, date, gamemap, gametype, speed, comment , 'At what Time should the next Tournament start?', 'pm' , 'pm', 'pm', 'pm' , 'pm', 'pm')





    # mysqlfunctions.add_tournament_tournament(date, time, gamemap, gametype, speed, comment)
    #mysqlfunctions.add_userscore_tournament()


    # comment = ""
    #
    # await ctx.send("Tournament added")
    # try:
    #     channel = ctx.guild.get_channel(733373412621156464)
    #     await channel.send("```New Tournament on the "+date + " at " + time +" \nGood Luck" + "\n"+comment+"```")
    # except:
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     traceback.print_exception(exc_type, exc_value, exc_traceback)
    #     await ctx.send("no such channel")


#--------------------------------------------



@client.command( aliases=["register"])
async def registerUser(ctx, battletag, name, nickname=""):
        mysqlfunctions.add_register(battletag, ctx.author.name + "#" + ctx.author.discriminator, name, nickname)
        await ctx.send("user " + ctx.author.name + " added")
        try:
            role = get(ctx.guild.roles, name='Users')
            await ctx.message.author.add_roles(role)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)


@client.command( aliases=["participate"])
async def participateUser(ctx):
    try:
        mysqlfunctions.add_participate(ctx.author.name + "#" + ctx.author.discriminator)
        await ctx.send("You are registered as Participant for the next Tournament. Good Luck!")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        await ctx.send("an Error occurred you might not be a user in the database yet. Please contact us")


#error handeling

@registerUser.error
async def on_command_error(ctx , error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("you might be missing an argument")
    else:
        await ctx.send("an unknown Error occurred. Please contact one of our staff members")
        print(error)

@Rudolf.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("you might be missing an argument")
    else:
        await ctx.send("an unknown Error occurred. Please contact one of our staff members")
        print(error)



client.run(pw.get_bot_token())

