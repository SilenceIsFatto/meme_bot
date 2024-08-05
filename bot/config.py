import discord
from discord import app_commands

from datetime import date
from datetime import datetime

import os

# Need to convert most of the variables in this file to json, that way we can add/remove during runtime

#https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
def format_embed(interaction=None, author=None, title=None, description=None, type="rich", colour=15844367, thumbnail="", footer="Cat Memes"):

    if (interaction == None and author == None):
        raise Exception("No interaction or user given in format_embed.")

    if (interaction != None):
        author_name = interaction.user.name
        author_id = interaction.user.id
    else:
        author_name = author.name
        author_id = author.id

    # log_message(2, f"{author_name} ({author_id}) is sending an embedded message.", space=True)
    # log_message(2, f"Title: {title}")
    # log_message(2, f"Colour: {colour}")
    # log_message(2, f"Thumbnail: {thumbnail}")

    embed_message = discord.Embed(title=title, description=description, type=type, colour=colour)
    embed_message.set_thumbnail(url=thumbnail)
    embed_message.set_footer(text=footer)
    return embed_message

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

guild_reddit_default_subreddits = ["Catmemes", "dogmemes", "capybara"]

def guild_reddit_link(random_meme, meme_link):
    url = f"[{random_meme[1]}]({random_meme[2]}) - [Link](<{meme_link}>)"

    return url

def guild_reddit_embed(subreddit_name=None, interaction=None, random_meme=None, meme_link=None):
    subreddit_name_r = f"r/{subreddit_name}"
    embed = format_embed(interaction=interaction, title=random_meme[1], description=f"[Link](<{meme_link}>)", footer=subreddit_name_r)

    embed.set_image(url=random_meme[2])

    return embed

def guild_reddit_embed_send(subreddit_name=None, interaction=None, random_meme=None, meme_link=None):
    embed_send = interaction.response.send_message(embed=guild_reddit_embed(subreddit_name=subreddit_name, interaction=interaction, random_meme=random_meme, meme_link=meme_link))

    return embed_send

def guild_log_spacer(message):
    spacer = f"\--------- {message} ---------/"

    return spacer

def url_missing(interaction, local=True):
    return interaction.response.send_message("This URL doesn't exist or is returning 404.", ephemeral=local)

async def shutdown(client):
    print(f"We have logged out of {client.user}. ID: {client.user.id}")
    
    await client.close() # probably best to await the client to close itself, as it spams errors before shutting down otherwise

    exit()