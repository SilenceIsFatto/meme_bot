import sys

sys.path.append("../")

from file_operations import write_to_file

setting_debug_level = 0

from config import guild_log_file
from config import guild_day_time

def log_message(debug_level=-1, message=None, header="General", space=False):
    if (debug_level == -1 and setting_debug_level <= 10):
        print(f"{message}")

        day = guild_day_time("day")
        time = guild_day_time("time", "%H:%M:%S")

        message = f"[{day} {time}] [INFO Cat Memes] | {header} | {message}"
        
        if (space):
            message = f"\n{message}"

        write_to_file(guild_log_file, [message], "a+")

    if (debug_level == 0 and setting_debug_level == debug_level):
        print(f"\nInformation: {message}")

    if (debug_level >= 1 and setting_debug_level == debug_level):
        print(f"\nData: {message}")