from functions.main import start_reddit_instance
from functions.get_meme import get_submissions_thread

import time

import os

# pulls memes every timer:seconds
def json_loop(timer=604800):

    while (True):

        # redundancy, .on gets created when the bot goes online and deleted when offline
        if (os.path.isfile(".on")):
            pass
        else:
            break

        subreddit = start_reddit_instance()
        get_submissions_thread(subreddit=subreddit)

        time.sleep(timer)

if (__name__ == "__main__"):
    json_loop()