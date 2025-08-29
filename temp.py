import os
from discord import *
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

load_dotenv()

FFMPEG_OPTS = {'before_options': '-reconnect 1 -rtbufsize 500M', 'options': '-vn'}

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)

current_voice = None
music_queue = []
current_song = None

@tree.command(
    name="ping",
    description="ping pong",
    guild=Object(id=GUILD)
)
@app_commands.describe(arg1="argument test")
async def ping(interaction, arg1: str):
    await interaction.response.send_message(f"pong {arg1}")

@tree.command(
    name="play",
    description="play a song",
    guild=Object(id=GUILD)
)
@app_commands.describe(search="youtube video url")
async def play(interaction, search: str):
    global music_queue
    global current_song

    if current_voice == None:
        await interaction.response.send_message(f"i must be in a channel to play music, use /join first")
        return

    text_chan = interaction.channel
    ydl_opts_proc = {'format': 'bestaudio/best', 'extract_flat': False}
    ydl_opts = {'format': 'bestaudio', 'audio-format': 'opus', 'extract_flat': True}

    await interaction.response.send_message(f"searching for '{search}' . . .")
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)
    with YoutubeDL(ydl_opts_proc) as ydl_proc:
        proc_info = ydl_proc.extract_info(f"ytsearch:{search}", download=False)
    url_retrieved = info['entries'][0]['url']
    proc_url = proc_info['entries'][0]['url']
    #print(proc_url)
    print(url_retrieved)
    print(info)
    songtitle = info['entries'][0]['title']
    await text_chan.send(f"adding [{songtitle}](<{url_retrieved}>) to the queue")

    music_queue.append((proc_url, url_retrieved, songtitle))

    print("before")
    if current_voice.is_playing() == False:
        print("after")
        play_next(interaction)
    
def play_next(interaction):
    global current_song
    ffmpeg_opts = {'before_options': '-reconnect 1 -rtbufsize 500M', 'options': '-vn'}
    print("song finished")
    if len(music_queue) == 0:
        return
    current_song = music_queue.pop(0)
    next_url = current_song[0]
    current_voice.play(FFmpegOpusAudio(next_url, **ffmpeg_opts,), after=lambda e: play_next(interaction))
    
    
@tree.command(
    name="stop",
    description="stops all music and clears the queue",
    guild=Object(id=GUILD)
)
async def stop(interaction):
    global current_song
    global music_queue
    music_queue = []
    current_song = None
    current_voice.stop()
    await interaction.response.send_message("stopping music")

@tree.command(
    name="skip",
    description="skips the currently playing song",
    guild=Object(id=GUILD)
)
async def skip(interaction):
    global current_song
    current_voice.stop()
    await interaction.response.send_message(f"skipping [{current_song[2]}](<{current_song[1]}>)")

@tree.command(
    name="queue",
    description="shows the current queue",
    guild=Object(id=GUILD)
)
async def queue(interaction):
    global current_song
    global music_queue
    queue_string = ">>> "
    i = 0
    if current_song == None:
        await interaction.response.send_message("nothing playing!")
        return
    queue_string += f"`Playing` : [{current_song[2]}](<{current_song[1]}>)\n"
    if len(music_queue) == 0:
        await interaction.response.send_message(queue_string)
        return
    for s in music_queue:
        queue_string += f" `{i}` : [{s[2]}](<{s[1]}>)\n"
        i += 1
        
    await interaction.response.send_message(queue_string)

@tree.command(
    name="join",
    description="join your voice channel",
    guild=Object(id=GUILD)
)
async def join(interaction):
    global current_voice

    voicech_name = str(interaction.user.voice.channel)
    if current_voice != None:
        await interaction.response.send_message(f"i'm already in the channel {voicech_name}")
        return
    user_voicech_id = interaction.user.voice.channel.id
    if user_voicech_id == None:
        await interaction.response.send_message("you must be in a channel to use /join")
    user_voicech = client.get_channel(user_voicech_id)
    voice_client = await user_voicech.connect()
    current_voice = voice_client
    await interaction.response.send_message(f"joined channel {voicech_name}")

@tree.command(
    name="leave",
    description="make the bot disconnect",
    guild=Object(id=GUILD)
)
async def leave(interaction):
    global current_voice
    if current_voice == None:
        await interaction.response.send_message("i'm not in a channel")
        return
    await current_voice.disconnect()
    await interaction.response.send_message("goodbye")
    cleanup_after_leave()

@client.event
async def on_ready():
    await tree.sync(guild=Object(id=GUILD))
    print("ready")

@client.event
async def on_voice_state_update(member, state_before, state_after):
    global current_voice
    if current_voice == None or state_before == None:
        return
    if not (state_before.channel.id == current_voice.channel.id):
        return
    if len(state_before.channel.members) == 1:
        await current_voice.disconnect()
        cleanup_after_leave()

def cleanup_after_leave():
    global current_voice
    global music_queue
    global current_song
    current_song = None
    music_queue = []
    current_voice = None
    

client.run(TOKEN)