import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord import ui

import sys

from functions.get_meme import format_reddit_link

from typing import Literal

from functions.get_meme import subreddit_supported
from functions.get_meme import format_reddit_link
from functions.get_meme import grab_cat_meme

def commands_user(client, tree):

    @tree.command(name="user_send_meme")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def user_send_meme(interaction: discord.Interaction, subreddit_name: Literal["Catmemes", "dogmemes", "capybara"]) -> None:

        subreddit_added = subreddit_supported(guild_id=None, subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit is not supported for user installs.")

        random_meme = grab_cat_meme(subreddit=subreddit_name)

        meme_link = format_reddit_link(post_id=random_meme[0])

        await interaction.response.send_message(f"Reddit - [{random_meme[1]}]({random_meme[2]}) - [Link](<{meme_link}>)")

    @tree.command(name="user_send_cat_meme")
    @app_commands.allowed_installs(guilds=False, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) 
    async def user_send_cat_meme(interaction: discord.Interaction) -> None:
        
        random_meme = grab_cat_meme(subreddit="Catmemes")

        meme_link = format_reddit_link(post_id=random_meme[0])

        await interaction.response.send_message(f"Reddit - [{random_meme[1]}]({random_meme[2]}) - [Link](<{meme_link}>)")
    
    @user_send_meme.error
    @user_send_cat_meme.error
    async def say_error(interaction : discord.Interaction, error):
        await interaction.response.send(interaction, error, local=True)