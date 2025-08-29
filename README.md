# 🧱 brickbot 🧱

## About
Brickbot is a barebones python discord bot that can play Youtube videos using yt-dlp.

## Commands
All commands are discord slash commands.

```/play```: ```youtube search or url```
- adds a song to the music queue, the bot will join your voice channel if it isn't in one

```/join```
- makes the bot join your voice channel

```/leave```
- makes the bot leave its current discord channel

```/queue```
- displays the current music queue

```/swap```: ```song1 index``` ```song2 index```
- swaps the position of two songs in the queue based on index

```/ping```
- pong

## Installation

Clone the project, create a virtual environment and install the requirements in requirements.txt.

.env.example should be renamed to .env and filled with your bot token. You should be able to leave 'GUILD' empty, though commands might register quicker if you fill it with your Server ID.

If you're on Linux and have tmux installed, you can use ```startup.sh``` to start an instance of the bot. You should probably start the bot on some sort of host like Google or Oracle cloud, both of which offer free tiers for hosting. The bot might have choppy playback if you host it from your own home internet.

## TODO:
- Youtube playlist support
- 