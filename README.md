Requirements:
```
discord.py
praw
asyncio
icecream
```

## Manual Install:
Create a file to start the bot. This can be any file that will run the main.py file. In this case we're going to use .ps1

Name this file `[start].ps1` and inside of it place the code that will run main.py. Example: `py main.py`, `python main.py`

You can skip this if you want to run the file through the vscode terminal, etc.

### Token

Create a python file called `bot_token.py` in the `bot` folder and inside it add a variable:
```py
token = BOT_TOKEN 
```
Replace token with the bot token, as string