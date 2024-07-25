import praw

from functions.get_meme import get_subreddit, get_submissions

from functions.handle_json import read_json

def start_reddit_instance(subreddit_name=None, guild_id=None):

    if (subreddit_name == None):
        subreddit_name = get_subreddit(guild_id=guild_id)

    reddit = praw.Reddit(
        client_id="2Gl-Fy1aB7WsFt5Ltyp9zw",
        client_secret="cyuXfIHCxwtrpOSA3-p5dZHNOUhs_A",
        redirect_uri="https://www.reddit.com/r/Catmemes",
        user_agent="cat memes script",
    )

    subreddit = reddit.subreddit(subreddit_name)

    return subreddit
    
if (__name__ == "__main__"):
    subreddit = start_reddit_instance()
    get_submissions(subreddit=subreddit)