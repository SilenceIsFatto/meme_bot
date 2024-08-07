import discord
from discord.ext import commands, tasks
from discord import app_commands
import functions.get_meme
import os
import logging
import asyncio
from icecream import ic
from time import sleep
import sys

# sys.path.append("../cat-meme-bot")

from config import guild_log_file, guild_log_init, guild_id, guild_channel_meme, guild_lock_file

from bot_token import token
from functions.log import log_message
from functions.main import start_reddit_instance
from functions.get_meme import get_submissions_thread
from commands import commands_init

from functions.common import initialise_memes

from file_operations import write_to_file

if (not os.path.exists("logs")):
    os.makedirs("logs")

handler = logging.FileHandler(filename=guild_log_file, encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

async def meme_post_loop(timer=600):
    while (client.synced):
        await functions.get_meme.scheduled_cat_meme(client, guild_channel_meme)

        await asyncio.sleep(timer)

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents,)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        try:
            await self.wait_until_ready()

            log_message(-1, message=f'We have logged into Discord as {client.user}. ID: {client.user.id}\n', header=guild_log_init, space=True)
            if not self.synced:
                await tree.sync(guild=guild_id) # can cause rate limits, so need to be careful
                self.synced = True

            # await meme_post_loop()
        except Exception as exp:
            log_message(-1, (f"Something went wrong! {exp}"))
            
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='For Cat Memes'))

client = aclient()
tree = commands_init(client)

write_to_file(filename=guild_lock_file, data="", type="w")
initialise_memes()

client.run(token, log_handler=handler)

client.synced = False

os.remove(guild_lock_file)