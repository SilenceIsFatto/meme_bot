import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord import ui
import sys
from functions.log import log_message

from typing import Literal

import os

sys.path.append(f'../cat-meme-bot')

from config import guild_id, guild_reddit_link, guild_reddit_embed_send

from functions.handle_json import read_json
from functions.handle_json import update_json

from functions.select_random import select_random

from functions.main import start_reddit_instance

from functions.get_meme import subreddit_supported, grab_cat_meme, format_reddit_link
from functions.get_meme import get_subreddits, get_settings, get_submissions_thread

from commands_user import commands_user

def commands_init(client):

    tree = app_commands.CommandTree(client)

    commands_user(client=client, tree=tree)

    @tree.command(name="sync_commands", description="Syncs the command tree.", guild=guild_id)
    async def sync_commands(interaction: discord.Interaction, guild_only: bool = False):

        if (interaction.user.id not in [474144080801169418, 705425476142891038]):
            raise Exception("You can't use this command.")

        if (guild_only):
            await tree.sync(guild=guild_id)
        else:
            await tree.sync()

        await interaction.response.send_message(f"Synced commands.")

    @tree.command(name="update_subreddit", description="Refreshes posts from a subreddit. Use the subreddit name, not the whole link!", guild=guild_id)
    async def update_subreddit(interaction: discord.Interaction, subreddit_name: str):

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit hasn't been added.")

        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        subreddit = start_reddit_instance(subreddit_name=subreddit_name)
        get_submissions_thread(subreddit=subreddit)

        await interaction.response.send_message(f"Updating memes.json with new subreddit posts: {subreddit}")

    @tree.command(name="remove_subreddit", description="Removes a subreddit. Use the subreddit name, not the whole link!", guild=guild_id)
    async def remove_subreddit(interaction: discord.Interaction, subreddit_name: str):

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit has not been added. Try adding it with /add_subreddit")

        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        # has to be str or else the json will break eventually
        guild_id = str(interaction.guild.id)

        subreddits = get_subreddits(guild_id)
        subreddits.remove(subreddit_name)

        dict = {
            guild_id: {
                "subreddits": subreddits
            }
        }

        update_json(data=dict, file_name="settings")

        await interaction.response.send_message(f"Removed subreddit: {subreddit_name}")

    @tree.command(name="add_subreddit", description="Adds a new subreddit. Use the subreddit name, not the whole link!", guild=guild_id)
    async def add_subreddit(interaction: discord.Interaction, subreddit_name: str):

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (subreddit_added):
            raise Exception("This subreddit has already been added.")

        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        # has to be str or else the json will break eventually
        guild_id = str(interaction.guild.id)

        subreddits = get_subreddits(guild_id)
        subreddits.append(subreddit_name)

        dict = {
            guild_id: {
                "subreddits": subreddits
            }
        }

        update_json(data=dict, file_name="settings")

        subreddit = start_reddit_instance(subreddit_name=subreddit_name)
        get_submissions_thread(subreddit=subreddit)

        await interaction.response.send_message(f"Added a new subreddit: {subreddit_name}")

    @tree.command(name="meme", description="Sends a meme from a subreddit (if supported).", guild=guild_id)
    async def meme(interaction: discord.Interaction, subreddit_name: str):
        
        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit hasn't been added.")

        random_meme = grab_cat_meme(subreddit=subreddit_name)

        meme_link = format_reddit_link(post_id=random_meme[0])

        await guild_reddit_embed_send(subreddit_name=subreddit_name, interaction=interaction, random_meme=random_meme, meme_link=meme_link)

    @tree.command(name="cat_meme", description="Sends a cat meme.", guild=guild_id)
    async def cat_meme(interaction: discord.Interaction):

        subreddit_name = "Catmemes"

        random_meme = grab_cat_meme(subreddit=subreddit_name)

        meme_link = format_reddit_link(post_id=random_meme[0])

        await guild_reddit_embed_send(subreddit_name=subreddit_name, interaction=interaction, random_meme=random_meme, meme_link=meme_link)

    @sync_commands.error
    @update_subreddit.error
    @remove_subreddit.error
    @add_subreddit.error
    @meme.error
    @cat_meme.error
    async def say_error(interaction : discord.Interaction, error):
        await interaction.response.send_message(error, ephemeral=True)

    return tree