import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord import ui
import sys
from functions.log import log_message

from typing import Literal

import os

sys.path.append(f'../cat-meme-bot')

from config import guild_id, guild_reddit_link, guild_reddit_embed_send, guild_reddit_default_subreddits

from functions.handle_json import read_json
from functions.handle_json import update_json

from functions.select_random import select_random

from functions.main import start_reddit_instance

from functions.get_meme import subreddit_supported, grab_cat_meme, format_reddit_link
from functions.get_meme import get_subreddits, get_settings, get_submissions_thread

def commands_init(client):

    tree = app_commands.CommandTree(client)

    # commands_user(client=client, tree=tree)

    @tree.command(name="sync_commands", description="Syncs the command tree.", guild=guild_id)
    async def sync_commands(interaction: discord.Interaction, guild_only: bool = False):

        if (interaction.user.id not in [474144080801169418, 705425476142891038]):
            raise Exception("You can't use this command.")

        if (guild_only):
            await tree.sync(guild=guild_id)
        else:
            await tree.sync()

        await interaction.response.send_message(f"Synced commands.")

    @tree.command(name="subreddit_update", description="Refreshes posts from a subreddit. Use the subreddit name, not the whole link!")
    async def subreddit_update(interaction: discord.Interaction, subreddit_name: str):

        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit hasn't been added.")

        subreddit = start_reddit_instance(subreddit_name=subreddit_name)
        get_submissions_thread(subreddit=subreddit)

        await interaction.response.send_message(f"Updating memes.json with new subreddit posts: {subreddit}")

    @tree.command(name="subreddit_list", description="Lists this servers supported subreddits.")
    async def subreddit_list(interaction: discord.Interaction):

        subreddits = get_subreddits(guild_id=(interaction.guild.id))

        await interaction.response.send_message(f"Supported subreddits in '{interaction.guild.name}': `{subreddits}`")
        
    @tree.command(name="subreddit_remove", description="Removes a subreddit. Use the subreddit name, not the whole link!")
    async def subreddit_remove(interaction: discord.Interaction, subreddit_name: str):

        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit has not been added. Try adding it with /add_subreddit")

        # has to be str or else the json will break eventually
        guild_id = str(interaction.guild.id)

        subreddits = get_subreddits(guild_id)
        subreddits.remove(subreddit_name)

        guild_name = interaction.guild.name
        dict = {
            guild_id: {
                "name": guild_name,
                "subreddits": subreddits
            }
        }

        update_json(data=dict, file_name="settings")

        await interaction.response.send_message(f"Removed subreddit: {subreddit_name}")

    @tree.command(name="subreddit_add", description="Adds a new subreddit. Use the subreddit name, not the whole link!")
    async def subreddit_add(interaction: discord.Interaction, subreddit_name: str):

        # Can make this its own function, cba repeating it in future
        if (subreddit_name in ["https://", "reddit.com"]):
            raise Exception("Don't give the whole link, only provide the subreddit name!")

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (subreddit_added):
            raise Exception("This subreddit has already been added.")

        # has to be str or else the json will break eventually
        guild_id = str(interaction.guild.id)

        subreddits = get_subreddits(guild_id)
        subreddits.append(subreddit_name)

        guild_name = interaction.guild.name
        dict = {
            guild_id: {
                "name": guild_name,
                "subreddits": subreddits
            }
        }

        update_json(data=dict, file_name="settings")

        subreddit = start_reddit_instance(subreddit_name=subreddit_name)
        get_submissions_thread(subreddit=subreddit)

        await interaction.response.send_message(f"Added a new subreddit: {subreddit_name}")

    @tree.command(name="image", description="Sends a random image from a provided subreddit (if supported).")
    async def image(interaction: discord.Interaction, subreddit_name: str):

        # if (interaction.is_user_integration):
            # if (subreddit_name not in guild_reddit_default_subreddits):
                # raise Exception(f"User installs are limited to: {guild_reddit_default_subreddits}. Please use one of them instead or alternatively add the bot to your server.")

        subreddit_added = subreddit_supported(guild_id=(interaction.guild.id), subreddit_name=subreddit_name)

        if (not subreddit_added):
            raise Exception("This subreddit hasn't been added.")

        random_meme = grab_cat_meme(subreddit=subreddit_name)

        meme_link = format_reddit_link(post_id=random_meme[0])

        await guild_reddit_embed_send(subreddit_name=subreddit_name, interaction=interaction, random_meme=random_meme, meme_link=meme_link)

    @tree.command(name="image_cat", description="Sends a random cat image from r/Catmemes.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cat_meme(interaction: discord.Interaction):

        subreddit_name = "Catmemes"

        random_meme = grab_cat_meme(subreddit=subreddit_name)

        meme_link = format_reddit_link(post_id=random_meme[0])

        await guild_reddit_embed_send(subreddit_name=subreddit_name, interaction=interaction, random_meme=random_meme, meme_link=meme_link)
        
    @tree.command(name="update", description="Sends instructions on how to update the user installed Cat Memes app.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def update(interaction: discord.Interaction):

        await interaction.response.send_message(content=f"Updates should happen automatically. If they don't happen, reauthorize the Cat Memes app.", ephemeral=True)

    @sync_commands.error
    @subreddit_update.error
    @subreddit_list.error
    @subreddit_remove.error
    @subreddit_add.error
    @image.error
    @cat_meme.error
    @update.error
    async def say_error(interaction : discord.Interaction, error):
        await interaction.response.send_message(error, ephemeral=True)

    return tree