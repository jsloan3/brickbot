# config.py
import os
from dotenv import load_dotenv

load_dotenv()
### CONSTANTS ###
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in .env")

GUILD = os.getenv('GUILD_ID')
if not GUILD:
    GUILD = None

FFMPEG_OPTS = {'before_options': '-reconnect 1 -rtbufsize 500M', 'options': '-vn'}
YDL_OPTS = {
    'format': 'bestaudio/best', 
    'extract_flat': False,
    'cookiefile': 'cookies.txt'
}
########################