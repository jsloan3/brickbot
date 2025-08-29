from song import Song
import discord
from discord import *
import voice
from config import FFMPEG_OPTS

class PlayerManager:
    def __init__(self, voice_client: voice.VoiceManager):
        self.voice_client = voice_client
        self.current_song: Song = None
        self.music_queue = []


    async def add_song(self, interaction: discord.Interaction, search: str):
        text_channel = interaction.channel
        if self.voice_client.voice_connection == None:
            await self.voice_client.join(interaction)
            await text_channel.send(f"searching for '{search}' . . .")
        else:
            await interaction.response.send_message(f"searching for '{search}' . . .")

        new_song = Song(search)
        await text_channel.send(f"adding [{new_song.get_title()}](<{new_song.get_url()}>) to the queue")
        self.music_queue.append(new_song)
        if self.current_song == None:
            self.play_next()


    def play_next(self):
        if len(self.music_queue) == 0:
            self.current_song = None
            return
        self.current_song = self.music_queue.pop(0)
        self.voice_client.voice_connection.play(
            FFmpegOpusAudio(self.current_song.source, **FFMPEG_OPTS,),
                after=lambda e: self.play_next())


    async def stop(self, interaction: discord.Interaction):
        self.music_queue = []
        self.current_song = None
        self.voice_client.voice_connection.stop()
        await interaction.response.send_message("stopping music")


    async def skip(self, interaction: discord.Interaction):
        self.voice_client.voice_connection.stop()
        await interaction.response.send_message(f"skipping [{self.current_song.get_title()}](<{self.current_song.get_url()}>)")


    async def queue(self, interaction: discord.Interaction):
        if self.current_song == None:
            await interaction.response.send_message("nothing playing!")
            return
        queue_string = ">>> "
        queue_string += f"`Playing` : [{self.current_song.get_title()}](<{self.current_song.get_url()}>)\n"
        if len(self.music_queue) == 0:
            await interaction.response.send_message(queue_string)
            return
        for i, s in enumerate(self.music_queue):
            queue_string += f" `{i}` : [{s.get_title()}](<{s.get_url()}>)\n"
        await interaction.response.send_message(queue_string)


    async def swap(self, interaction: discord.Interaction, song1: str, song2: str):
        if self.current_song == None:
            await interaction.response.send_message("nothing playing!")
            return
        self.music_queue[int(song1)], self.music_queue[int(song2)] = self.music_queue[int(song2)], self.music_queue[int(song1)]
        await interaction.response.send_message(f"swapped songs [{self.music_queue[int(song1)].get_title()}](<{self.music_queue[int(song1)].get_url()}>) and [{self.music_queue[int(song2)].get_title()}](<{self.music_queue[int(song2)].get_url()}>)")


    
    
