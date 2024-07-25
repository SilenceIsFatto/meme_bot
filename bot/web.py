import discord

from functions.log import log_message

#https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
def format_embed(interaction=None, author=None, title=None, description=None, type="rich", colour=15844367, thumbnail="", footer="Fat"):

    if (interaction == None and author == None):
        raise Exception("No interaction or user given in format_embed.")

    if (interaction != None):
        author_name = interaction.user.name
        author_id = interaction.user.id
    else:
        author_name = author.name
        author_id = author.id

    log_message(2, f"{author_name} ({author_id}) is sending an embedded message.", space=True)
    log_message(2, f"Title: {title}")
    log_message(2, f"Colour: {colour}")
    log_message(2, f"Thumbnail: {thumbnail}")

    embed_message = discord.Embed(title=title, description=description, type=type, colour=colour)
    embed_message.set_thumbnail(url=thumbnail)
    embed_message.set_footer(text=footer)
    return embed_message

def send_message(interaction, message, local=False, just_message=False):    
    try:
        if (local == False):    
            log_message(1, (f"{interaction.user.name} is sending a message: {message}"))

        if (just_message):
            return message
            
        return interaction.response.send_message(message, ephemeral=local)
    except: # should probably add a proper exception here
        log_message(-1, (f"Could not send message. {message}"))