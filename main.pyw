import discord
from discord.ext import commands
import datetime

client = commands.Bot(command_prefix='!')

settings = {
    "token": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Replace with your token
    "custom_status": {
        "start": datetime.datetime(2011, 11, 18), # Starting date of playing the game
        "name": "Minecraft",  # Name of the game
        "status": discord.Status.online}  # Status of the bot
}


@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}#{client.user.discriminator}')

    days = (datetime.datetime.now() - settings["custom_status"]["start"]).days
    hours = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds // 3600
    minutes = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds // 60 % 60
    seconds = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds % 60

    print("Playing the game '" + settings["custom_status"]["name"] + "' for " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
    # Creating a custom activity
    custom_activity=discord.Game(name = name, start = settings["custom_status"]["start"])

    # Changing the status of the bot
    await client.change_presence(activity = custom_activity, status = settings["custom_status"]["status"])

client.run(settings["token"], bot = False)
