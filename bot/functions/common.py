import os
from file_operations import write_to_file

from functions.handle_json import read_json
from functions.main import start_reddit_instance
from functions.get_meme import get_submissions_thread

def initialise_memes():

    subreddits = read_json(file_name="settings", key="subreddits", value_default=[])

    for subreddit_name in subreddits:

        subreddit = start_reddit_instance(subreddit_name=subreddit_name)
        get_submissions_thread(subreddit=subreddit)