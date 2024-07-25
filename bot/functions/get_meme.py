# from select_random import select_random
import sys
import os

from functions.handle_json import read_json, update_json
from functions.threads import *
from datetime import datetime
from functions.log import log_message

import random

file_json = "memes"

submissions_dict = {}

def select_random(array):
    data = array[random.randrange(0, len(array))]
    return data

def format_reddit_link(subreddit=None, post_id=None):
    if (subreddit == None):
        subreddit = get_subreddit()

    return f"https://www.reddit.com/r/{subreddit}/comments/{post_id}"

def subreddit_supported(guild_id=None, subreddit_name=None):
    if (guild_id == None):
        settings = get_settings()
        subreddits = settings["subreddits"]
    else:
        subreddits = get_subreddits(guild_id=guild_id)

    if (subreddit_name not in subreddits):
        return False

    return True

def get_settings():
    settings = read_json("settings")

    return settings

def get_subreddits(guild_id):
    guild_id = str(guild_id)
    settings = get_settings()
    setting_guild = settings.get(guild_id, None)

    setting_subreddits = []

    if (setting_guild != None):
        setting_subreddits = settings[guild_id].get("subreddits", [])

    subreddits = setting_subreddits

    return subreddits

def get_subreddit(guild_id=None):
    settings = get_settings()

    if (guild_id != None):
        setting_subreddit = settings[guild_id].get("subreddits", [])

        if (setting_subreddit == []):
            pass
        else:
            return setting_subreddit

    setting_subreddit = settings["subreddit"]
    return setting_subreddit

def get_submissions_json():
    submissions_dict = read_json(file_name=file_json)

    return submissions_dict

def get_submissions_thread(subreddit=None, submission_amount=1000):
    log_message(-1, "Running submissions thread")
    thread_function(target=get_submissions, args=(subreddit, submission_amount), start_thread=True)

def get_submissions(subreddit=None, submission_amount=1000):
    submissions = 0
    subreddit_submissions = subreddit.top(time_filter="all", limit=None)

    subreddit_name = str(subreddit)

    submissions_dict = {subreddit_name: {}}
        
    for subreddit_submission in subreddit_submissions:      
        sub_id = subreddit_submission.id
        title = subreddit_submission.title
        url = subreddit_submission.url
        time_created = subreddit_submission.created_utc

        #to be used later for time checking
        c_time = datetime.fromtimestamp(time_created).strftime('%Y-%m-%d %H:%M:%S')
        if ("i.redd.it" not in url):
            continue

        submissions_dict[subreddit_name].update({sub_id: {"title": title, "url": url}})

        submissions += 1

    update_json(data=submissions_dict, file_name=file_json)

def grab_cat_memes(subreddit=None):
    memes = []
    submissions_dict = read_json(file_name="memes")
    submissions_dict_seen = read_json(file_name="seen")

    if (subreddit == None):
        subreddit = get_subreddit()

    for sub_id in submissions_dict[subreddit].keys():
        title = submissions_dict[subreddit][sub_id]["title"]
        meme = submissions_dict[subreddit][sub_id]["url"]
        sub_id_seen = submissions_dict_seen.get(sub_id, None)

        if (sub_id_seen == None):
            seen = False
        else:
            seen = sub_id_seen.get("seen", False)

        if seen:
            pass
        else:
            memes.append([sub_id, title, meme, seen])

    return memes

def grab_cat_meme(memes=[], subreddit=None):
    if (memes == []):
        memes = grab_cat_memes(subreddit=subreddit)
        # if memes still returns nothing, we're unfortunately out of unique memes
        if (memes == []):
            log_message(-1, "out of memes")
            return ["No memes were found :(", "https://www.reddit.com/r/Catmemes/"]

    random_meme = select_random(memes)

    subreddit_name = str(subreddit)

    if (random_meme[3] == False):
        
        dict = {
            random_meme[0]: {
                "seen": True
            }
        }
        
        update_json(data=dict, file_name="seen")

        return random_meme

async def scheduled_cat_meme(client, guild_channel=None):
    channel = client.get_channel(guild_channel)

    random_meme = grab_cat_meme(subreddit="Catmemes")

    meme_link = format_reddit_link(post_id=random_meme[0])
    message = f"Reddit - [{random_meme[1]}]({random_meme[2]}) - [Link](<{meme_link}>)"

    await channel.send(message)
    log_message(-1, f"sent {message}")