import os
from file_operations import write_to_file

from functions.handle_json import read_json
from functions.main import start_reddit_instance
from functions.get_meme import get_submissions_thread

import sys
import subprocess

def initialise_memes():

    subprocess.Popen(f"python bot\\functions\\json_loop.py")