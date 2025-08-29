# main.py
import discord
from discord import *
from voice import VoiceManager
from player_manager import PlayerManager
from config import TOKEN, GUILD

### GLOBAL VARIABLES ###
client = discord.Client(intents=discord.Intents.default())
main_voice = VoiceManager(client)
main_player = PlayerManager(main_voice)
tree = app_commands.CommandTree(client)
########################

@client.event
async def on_ready():
    # Import and setup commands module
    import commands
    commands.setup_commands(tree, client, main_voice, main_player)
    # Sync the tree with the guild
    await tree.sync(guild=Object(id=GUILD))
    print("ready")

@client.event
async def on_voice_state_update(member: discord.Member, state_before: discord.VoiceState,
 state_after: discord.VoiceState):
    if main_voice.voice_connection == None or state_before == None:
        return
    if not (state_before.channel.id == main_voice.voice_connection.channel.id):
        return
    if len(state_before.channel.members) == 1:
        await main_voice.disconnect()

# Only run if this file is run directly (not imported)
if __name__ == "__main__":
    client.run(TOKEN)