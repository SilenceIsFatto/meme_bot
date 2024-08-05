import discord

from functions.log import log_message

def send_message(interaction, message, local=False, just_message=False):    
    try:
        if (local == False):    
            log_message(1, (f"{interaction.user.name} is sending a message: {message}"))

        if (just_message):
            return message
            
        return interaction.response.send_message(message, ephemeral=local)
    except: # should probably add a proper exception here
        log_message(-1, (f"Could not send message. {message}"))