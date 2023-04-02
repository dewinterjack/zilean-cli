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
from discord_py_speech_recognition import DiscordPCMReceiver

import answers
import gpt
import speech_answer
import whisper

discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.3.1/lib/libopus.0.dylib')

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

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
        voice_client = await voice_channel.connect()

    receiver = DiscordPCMReceiver(voice_client)
    while True:
        audio_data = await receiver.get_next_data_frame()

        # Check for the audio cue - hey, zilean
        if whisper.check_for_audio_cue(audio_data):
            break

    await interaction.response.send_message("Zilean is listening")

    await listen_and_record(voice_client, duration=5)

    await interaction.response.send_message.send("Question saved")

async def listen_and_record(voice_client, duration):
    buffer = io.BytesIO()
    receiver = DiscordPCMReceiver(voice_client)

    try:
        while duration > 0:
            audio_data = await receiver.get_next_data_frame()
            buffer.write(audio_data)
            duration -= 0.02
    except asyncio.TimeoutError:
        pass

    buffer.seek(0)
    audio = AudioSegment.from_file(buffer, format="raw", channels=2, sample_width=2, frame_rate=48000)
    audio.export("recorded.wav", format="wav")
# @bot.command()
# async def leave(ctx):
#     await ctx.voice_client.disconnect()


# @bot.command()
# async def play2(ctx):
#     # Play the WAV buffer in the voice channel
#     voice_client = ctx.voice_client
#     if voice_client:
#         try:
#             audio_source = discord.FFmpegPCMAudio('test.mp3')
#             voice_client.play(audio_source)
#             await ctx.send('Playing audio...')
#         except Exception as e:
#             await ctx.send(f'Error playing audio: {e}')


# @bot.command()
# async def play(ctx):
#     # Play the WAV buffer in the voice channel
#     voice_client = ctx.voice_client
#     if voice_client:
#         audio_source = discord.FFmpegPCMAudio('test.mp3')
#         voice_client.play(audio_source)
#     await ctx.send('Playing audio...')


# @bot.command()
# async def status(ctx):
#   if ctx.voice_client is None or not
#     ctx.voice_client.is_connected():
#     await ctx.send("Bot is not connected to a voice channel. Use the `join` command first.")
#     return

client.run(
    'token')
