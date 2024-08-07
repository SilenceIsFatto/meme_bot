import praw

from functions.get_meme import get_subreddit, get_submissions

from functions.handle_json import read_json

from bot_token import reddit_client

def start_reddit_instance(subreddit_name=None, guild_id=None):

    if (subreddit_name == None):
        subreddit_name = get_subreddit(guild_id=guild_id)

    reddit = praw.Reddit(
        client_id=reddit_client[0],
        client_secret=reddit_client[1],
        redirect_uri=reddit_client[2],
        user_agent=reddit_client[3],
    )

    subreddit = reddit.subreddit(subreddit_name)

    return subreddit
    
if (__name__ == "__main__"):
    subreddit = start_reddit_instance()
    get_submissions(subreddit=subreddit)