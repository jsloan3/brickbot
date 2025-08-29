import discord
class VoiceManager:
    def __init__(self, bot_client: discord.Client):
        self.voice_connection = None
        self.bot_client = bot_client
    
    async def join(self, interaction: discord.Interaction):
        voicech_name = str(interaction.user.voice.channel)
        user_voicech_id = interaction.user.voice.channel.id
        
        if self.voice_connection != None:
            await interaction.response.send_message(f"i'm already in the channel {voicech_name}")
            return
        
        if user_voicech_id == None:
            await interaction.response.send_message("you must be in a channel to use /join")
            return
        
        user_voicech = self.bot_client.get_channel(user_voicech_id)
        self.voice_connection = await user_voicech.connect()

        await interaction.response.send_message(f"joined channel {voicech_name}")

    async def leave(self, interaction: discord.Interaction):
        if self.voice_connection == None:
            await interaction.response.send_message("i'm not in a channel")
            return
        await self.voice_connection.disconnect()
        await interaction.response.send_message("goodbye")
        self.voice_connection = None

    async def disconnect(self):
        await self.voice_connection.disconnect()
        self.voice_connection = None
        