from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPTLAYER_API_KEY = os.getenv("PROMPTLAYER_API_KEY")

import discord
from discord import app_commands
import io
import asyncio
from pydub import AudioSegment


import answers
import gpt
import speech_answer
import whisper

discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.3.1/lib/libopus.0.dylib')

channel = 1

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.zil_voice_client = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
            for command in synced:
                print(f"/{command.name}")
        except Exception as e:
            print(e)

intents = discord.Intents.default()
intents.message_content = True
client = DiscordClient(intents=intents)

async def ask_api(prompt: str):
    search_reddit = answers.get_comments(prompt)
    zilean_answer = gpt.ask(search_reddit).choices[0].message.content
    speech_answer.generate_speech_file(zilean_answer)
    audio_source = discord.FFmpegPCMAudio('zil_answer.mp3')
    client.zil_voice_client.play(audio_source)

@client.tree.command(name="ask", description="Ask a question about League of Legends item data.")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("Asking Zilean...", ephemeral=True)
    search_reddit = answers.get_comments(prompt)
    zilean_answer = gpt.ask(search_reddit).choices[0].message.content
    speech_answer.generate_speech_file(zilean_answer)
    guild = interaction.guild
    if guild:
        voice_client = guild.voice_client

    voice_channel = interaction.user.voice.channel
    if voice_client is None:
        
        voice_client = await voice_channel.connect()
        audio_source = discord.FFmpegPCMAudio('zil_answer.mp3')
        await interaction.followup.send("Now playing the answer in your voice channel.")
        voice_client.play(audio_source)
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)

@client.tree.command(name="listen", description="Answer questions when I say, Hey, Zilean.")
async def listen(interaction: discord.Interaction):
    guild = interaction.guild
    if guild:
        voice_client = guild.voice_client

    voice_channel = interaction.user.voice.channel
    
    if voice_client is None:
        client.zil_voice_client = await voice_channel.connect()

    

