import discord
from discord.ext import commands
import datetime
import json
import os

client = commands.Bot(command_prefix='!')

emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
message = None


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
    with open(os.path.join(directory, "settings.json"), "r") as f:
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
        if settings["custom_status"]["status"] not in settings["custom_status"]["possible_statuses"]:
            print("settings.json is not valid, please fix it or delete it, then restart the bot.")
            exit()

if not os.path.isfile(os.path.join(directory, "dump.txt")):
    with open(os.path.join(directory, "dump.txt"), "w") as f:
        f.write("")


    


@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}#{client.user.discriminator}')

    time = datetime.datetime(*settings["custom_status"]["start"])

    days = (datetime.datetime.now() - time).days
    hours = (datetime.datetime.now() - time).seconds // 3600
    minutes = (datetime.datetime.now() - time).seconds // 60 % 60
    seconds = (datetime.datetime.now() - time).seconds % 60

    start = datetime.datetime(*settings["custom_status"]["start"])

    print("Playing the game '" + settings["custom_status"]["name"] + "' for " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
    # Creating a custom activity
    custom_activity=discord.Game(name = settings["custom_status"]["name"], start = start)

    # Changing the status of the bot
    await client.change_presence(activity = custom_activity, status = settings["custom_status"]["status"])

@client.command()
async def menu(ctx):
    # Creating a menu
    content = "```\n"
    content += "1. Change status\n"
    content += "2. Change game name\n"
    content += "3. Change game start date\n"
    content += "```"


    message = await ctx.send(content=content)
    for i in range(1, 4):
        await message.add_reaction(emojis[i-1])
    def check(reaction):
        return str(reaction.emoji) in emojis and reaction.message_id == message.id and reaction.user_id == ctx.author.id
    reaction = await client.wait_for('raw_reaction_add', check=check)
    index = emojis.index(str(reaction.emoji))
    await message.delete()
    if index == 0:
        content = "```\n"
        content += "1. Online\n"
        content += "2. Idle\n"
        content += "3. Do Not Disturb\n"
        content += "4. Invisible\n"
        content += "```"
        message = await ctx.send(content=content)
        for i in range(1, 5):
            await message.add_reaction(emojis[i-1])
        def check(reaction):
            return str(reaction.emoji) in emojis and reaction.message_id == message.id and reaction.user_id == ctx.author.id
        reaction = await client.wait_for('raw_reaction_add', check=check)
        index = emojis.index(str(reaction.emoji))
        await message.delete()
        if index == 0:
            settings["custom_status"]["status"] = "online"
        elif index == 1:
            settings["custom_status"]["status"] = "idle"
        elif index == 2:
            settings["custom_status"]["status"] = "dnd"
        elif index == 3:
            settings["custom_status"]["status"] = "invisible"
        with open(os.path.join(directory, "settings.json"), "w") as f:
            json.dump(settings, f, indent=4)
        await ctx.send("Status changed to " + settings["custom_status"]["status"])
    elif index == 1:
        content = "```\n"
        content += "Input the name of the game\n"
        content += "```"
        message = await ctx.send(content=content)
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        name_message = await client.wait_for('message', check=check)
        settings["custom_status"]["name"] = name_message.content
        with open(os.path.join(directory, "settings.json"), "w") as f:
            json.dump(settings, f, indent=4)
        await ctx.send("Game changed to " + settings["custom_status"]["name"])
    elif index == 2:
        content = "```\n"
        content += "Input the start date of the game as follows: year, month, day, hour, minute, second\n"
        content += "```"
        message = await ctx.send(content=content)
        def check(message):
            return message.author == ctx.author 
        message = await client.wait_for('message', check=check)
        list = message.content.split(",")
        try:
            settings["custom_status"]["start"] = (int(list[0]), int(list[1]), int(list[2]), int(list[3]), int(list[4]), int(list[5]))
        except ValueError:
            await ctx.send("Invalid date")
            return
        with open(os.path.join(directory, "settings.json"), "w") as f:
            json.dump(settings, f, indent=4)
        await ctx.send("Game start date changed to " + str(settings["custom_status"]["start"]))
    # Creating a custom activity
    start = datetime.datetime(*settings["custom_status"]["start"])
    custom_activity=discord.Game(name = settings["custom_status"]["name"], start = start)
    # Changing the status of the bot
    await client.change_presence(activity = custom_activity, status = settings["custom_status"]["status"])


try:
    client.run(settings["token"], bot = False)
except discord.LoginFailure:
    print("Invalid token, exiting.")
    exit()
