import sys

sys.path.append("bot")

from functions.main import start_reddit_instance
from functions.get_meme import get_submissions_thread
from functions.log import log_message
from functions.handle_json import read_json

import time

import os

# pulls memes every timer:seconds
def json_loop(timer=604800):

    while (True):

        log_message(-1, "Starting json loop!")

        # redundancy, .on gets created when the bot goes online and deleted when offline
        if (os.path.isfile(".on")):
            pass
        else:
            break

        subreddits = read_json(file_name="settings", key="subreddits", value_default=[])

        for subreddit_name in subreddits:

            subreddit = start_reddit_instance(subreddit_name=subreddit_name)
            get_submissions_thread(subreddit=subreddit)

        time.sleep(timer)

if (__name__ == "__main__"):
    json_loop()