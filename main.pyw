import discord
from discord.ext import commands
import datetime
import json
import os

client = commands.Bot(command_prefix='!')



default_settings = {
    "token": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", # Replace with your token
    "custom_status": {
        "start": (2011, 11, 18), # Starting date of playing the game
        "name": "Minecraft",  # Name of the game
        "possible_statuses": ["online", "idle", "dnd", "invisible"], # Possible statuses
        "status": "online"}  # Status of the bot
}


#create documents folder in the user dir if it doesn't exist
if not os.path.exists(os.path.join(os.path.expanduser("~"), "Documents")):
    os.makedirs(os.path.join(os.path.expanduser("~"), "Documents"))
if not os.path.exists(os.path.join(os.path.expanduser("~"), "Documents", "MarqSelfbot")):
    os.makedirs(os.path.join(os.path.expanduser("~"), "Documents", "MarqSelfbot"))
directory = os.path.join(os.path.expanduser("~"), "Documents", "MarqSelfbot")

print("Settings.json location: " + directory)

if not os.path.isfile(os.path.join(directory, "settings.json")):
    with open(os.path.join(directory, "settings.json"), "w") as f:
        json.dump(default_settings, f, indent=4)
        print(f"Created settings.json in {directory}, please edit it and restart the bot.")
        exit()
else:
    with open("settings.json", "r") as f:
        try:
            settings = json.load(f)
            #if all keys and subkeys are in the settings, we're good
            if all(key in settings for key in default_settings):
                if all(key in settings["custom_status"] for key in default_settings["custom_status"]):
                    pass
                else:
                    raise json.decoder.JSONDecodeError("custom_status is missing keys", "", 0)
            else:
                raise json.decoder.JSONDecodeError("settings is missing keys", "", 0)

        except json.decoder.JSONDecodeError:
            print("settings.json is not valid JSON, please fix it or delete it, then restart the bot.")
            exit()
        settings["custom_status"]["start"] = datetime.datetime(*settings["custom_status"]["start"])
        if settings["custom_status"]["status"] not in settings["custom_status"]["possible_statuses"]:
            print("settings.json is not valid, please fix it or delete it, then restart the bot.")
            exit()




    


@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}#{client.user.discriminator}')

    days = (datetime.datetime.now() - settings["custom_status"]["start"]).days
    hours = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds // 3600
    minutes = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds // 60 % 60
    seconds = (datetime.datetime.now() - settings["custom_status"]["start"]).seconds % 60

    print("Playing the game '" + settings["custom_status"]["name"] + "' for " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
    # Creating a custom activity
    custom_activity=discord.Game(name = settings["custom_status"]["name"], start = settings["custom_status"]["start"])

    # Changing the status of the bot
    await client.change_presence(activity = custom_activity, status = settings["custom_status"]["status"])

client.run(settings["token"], bot = False)
