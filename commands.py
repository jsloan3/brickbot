# commands.py
import os
import discord
from discord import *
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from player_manager import PlayerManager
from config import GUILD
from voice import VoiceManager

class CommandManager:
    def __init__(self, cmd_tree, bot_client, voice_mgr, player_mgr):
        self.tree = cmd_tree
        self.client = bot_client
        self.main_voice = voice_mgr
        self.main_player = player_mgr
        self.setup_commands()
    
    def setup_commands(self):
        """Setup all the slash commands"""
        
        ### PING COMMAND ###
        @self.tree.command(
            name="ping",
            description="ping pong",
            guild=Object(id=GUILD)
        )
        @app_commands.describe(arg1="argument test")
        async def ping(interaction: discord.Interaction, arg1: str):
            await interaction.response.send_message(f"pong {arg1}")


        ### PLAY COMMAND ###
        @self.tree.command(
            name="play",
            description="play a song",
            guild=Object(id=GUILD)
        )
        @app_commands.describe(search="youtube video url")
        async def play(interaction, search: str):
            await self.main_player.add_song(interaction, search)
            return


        ### STOP COMMAND ###
        @self.tree.command(
            name="stop",
            description="stops all music and clears the queue",
            guild=Object(id=GUILD)
        )
        async def stop(interaction: discord.Interaction):
            await self.main_player.stop(interaction)
            return


        ### SKIP COMMAND ###
        @self.tree.command(
            name="skip",
            description="skips the currently playing song",
            guild=Object(id=GUILD)
        )
        async def skip(interaction: discord.Interaction):
            await self.main_player.skip(interaction)
            return


        ### QUEUE COMMAND ###
        @self.tree.command(
            name="queue",
            description="shows the current queue",
            guild=Object(id=GUILD)
        )
        async def queue(interaction: discord.Interaction):
            await self.main_player.queue(interaction)
            return


        ### JOIN COMMAND ###
        @self.tree.command(
            name="join",
            description="join your voice channel",
            guild=Object(id=GUILD)
        )
        async def join(interaction: discord.Interaction):
            await self.main_voice.join(interaction)
            return


        ### LEAVE COMMAND ###
        @self.tree.command(
            name="leave",
            description="make the bot disconnect",
            guild=Object(id=GUILD)
        )
        async def leave(interaction: discord.Interaction):
            await self.main_voice.leave(interaction)
            return


        ### SWAP COMMAND ###
        @self.tree.command(
            name="swap",
            description="swaps two songs in the queue",
            guild=Object(id=GUILD)
        )
        @app_commands.describe(
            song1="the index of the first song to swap",
            song2="the index of the second song to swap"
        )
        async def swap(interaction: discord.Interaction, song1: str, song2: str):
            await self.main_player.swap(interaction, song1, song2)
            return

# Global instance that will be set by main.py
command_manager = None

def setup_commands(cmd_tree, bot_client, voice_mgr, player_mgr):
    """Setup function to initialize commands with dependencies from main.py"""
    global command_manager
    command_manager = CommandManager(cmd_tree, bot_client, voice_mgr, player_mgr)
    return command_manager