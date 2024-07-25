import discord
from discord import app_commands

from datetime import date
from datetime import datetime

import os

# Need to convert most of the variables in this file to json, that way we can add/remove during runtime

def guild_day_time(type="", type_format=""):
    if (type == ""):
        exit()

    if (type == "day"):
        day = date.today()
        return day
    
    if (type == "time" and (type_format != "")):
        time = datetime.now().strftime(type_format)
        return time

    return False

day = guild_day_time("day")
time = guild_day_time("time", "%H-%M-%S")

guild_log_file = f"logs/{day}_{time}-discord.log"
guild_log_init = f"Bot initialization"

guild_lock_file = ".on"

guild_id = discord.Object(1262101726182244473)

guild_error_notmoderator = "You are not allowed to use this command."

guild_channel_meme = 1262370726279647293

def guild_log_spacer(message):
    spacer = f"\--------- {message} ---------/"

    return spacer

def url_missing(interaction, local=True):
    return interaction.response.send_message("This URL doesn't exist or is returning 404.", ephemeral=local)

async def shutdown(client):
    print(f"We have logged out of {client.user}. ID: {client.user.id}")
    
    await client.close() # probably best to await the client to close itself, as it spams errors before shutting down otherwise

    exit()