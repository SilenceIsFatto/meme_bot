import json
import os
import sys

sys.path.append("../bot")

from file_operations import write_to_file
from functions.log import log_message

# from common import initialise_memes

path = os.getcwd()

def json_exists(file):
    if (os.path.isfile(f"json/{file}.json")):
        return True
    else:
        try:
            os.makedirs(f"json")
        except:
            pass

    write_to_file(f"json/{file}.json", data="", type="w")

    if (file == "memes"):
        dict = {"init": {"title": "", "url": "", "seen": True}}

    if (file == "settings"):
        dict = {"subreddit": "Catmemes", "subreddits": ["Catmemes", "dogmemes", "capybara"]}

    if (file == "seen"):
        dict = {"init": {"seen": True}}

    save_json(dict, file_name=file)

def validate_key(dict, key, value_default):

    if (dict == value_default):
        raise KeyError(f"Key {key} was not found.")

def read_json(file_name, key="", value_default="default_return"):
    
    json_exists(file_name)

    with open(f'{path}/json/{file_name}.json', 'r') as file:

        read_file = file.read()
        dict = json.loads(read_file)

        if (key != ""):

            if (isinstance(key, list)): # if key is a list
                if (len(key) > 2): exit() # exit early if list has more than 2 elements

                dict = dict.get(key[0], value_default)

                validate_key(dict, key[0], value_default)

                try:
                    dict = dict[key[1]]
                    
                    return dict
                except KeyError:
                    raise KeyError(f"Key {key[1]} was not found. ( {key[0]} >> {key[1]} )")
                except:
                    raise Exception("Something went wrong.")

            dict = dict.get(key, value_default)

            validate_key(dict, key, value_default)
        else:
            return dict

    return dict

def save_json(data, file_name):

    json_exists(file_name)

    with open(f'{path}/json/{file_name}.json', 'w+') as file:
        json.dump(data, file, indent=4)

def update_json(data, file_name):

    json_exists(file_name)

    with open(f'{path}/json/{file_name}.json', 'r') as file:
        y = json.load(file)

    y.update(data)

    save_json(y, file_name)

    log_message(-1, f"Updated {file_name}.json")