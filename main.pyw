import discord
from discord.ext import commands
import datetime
client = commands.Bot()


token = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Replace with your token
start = datetime.datetime(2011, 11, 18) # Starting date of playing the game
name = "Minecraft" # Name of the game
status = discord.Status.online # Status of the bot



@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print("Playing the game: " + name + " for " + str(datetime.datetime.now() - start))")
    custom_activity = discord.Game(name=name, start=start) #Creating a custom activity

    await client.change_presence(activity=custom_activity, status=status) #Changing the status of the bot

client.run(token, bot=False)
