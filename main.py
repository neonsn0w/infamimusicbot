import os
import yt_dlp
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from collections import deque
import asyncio

import string_functions as sf

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# Song queues dict (a queue for each server!)
SONG_QUEUES = {}


async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))


def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')


@bot.tree.command(name="konami", description="You forgot the Konami Code, didnt you?")
async def konami(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Konami Code: :arrow_up: :arrow_up: :arrow_down: :arrow_down: :arrow_left: :arrow_right: :arrow_left: :arrow_right: :regional_indicator_b: :regional_indicator_a:",
        ephemeral=True)


@bot.tree.command(name="dementia", description="i forgor.")
async def dementia(interaction: discord.Interaction):
    await interaction.response.send_message(
        "https://cdn.discordapp.com/attachments/484399910280757250/1380274678379184239/dementia.mp4?ex=68434877&is=6841f6f7&hm=79d3325914cac39de0aca7c575fc44edc8581f482c88855133169bb5c2c2397b&",
        ephemeral=True)


@bot.tree.command(name="skip", description="Salta la canzone in riproduzione")
async def skip(interaction: discord.Interaction):
    if interaction.guild.voice_client and (
            interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Canzone saltata.", ephemeral=True)
    else:
        await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)


@bot.tree.command(name="pause", description="Metti in pausa la riproduzione.")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("Non sono in un canale vocale!", ephemeral=True)

    # Check if something is actually playing
    if not voice_client.is_playing():
        return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

    # Pause the track
    voice_client.pause()
    await interaction.response.send_message("Ho messo in pausa la riproduzione.", ephemeral=True)


@bot.tree.command(name="resume", description="Riprendi la riproduzione messa in pausa.")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if voice_client is None:
        return await interaction.response.send_message("Non sono in un canale vocale!", ephemeral=True)

    # Check if it's actually paused
    if not voice_client.is_paused():
        return await interaction.response.send_message("La riproduzione non è in pausa!", ephemeral=True)

    # Resume playback
    voice_client.resume()
    await interaction.response.send_message("Riprendo la riproduzione", ephemeral=True)


@bot.tree.command(name="nowplaying", description="Controlla che canzone è in riproduzione.")
async def nowplaying(interaction: discord.Interaction):
    if interaction.guild.voice_client is None or len(SONG_QUEUES) == 0 or len(
            SONG_QUEUES[str(interaction.guild_id)]) == 0:
        return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

    await interaction.response.send_message(f"Sto riproducendo:**{SONG_QUEUES[str(interaction.guild_id)][0][1]}**",
                                            ephemeral=True)


@bot.tree.command(name="queue", description="Visualizza la coda di riproduzione.")
async def queue(interaction: discord.Interaction):
    if interaction.guild.voice_client is None or len(SONG_QUEUES) == 0 or len(
            SONG_QUEUES[str(interaction.guild_id)]) == 0:
        return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

    queue_msg: str = "Ecco la coda:\n\n"

    for song in SONG_QUEUES[str(interaction.guild_id)]:
        queue_msg += f"- **{song[1]}**\n"

    await interaction.response.send_message(queue_msg, ephemeral=True)


@bot.tree.command(name="stop", description="Ferma la riproduzione.")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client

    # Check if the bot is in a voice channel
    if not voice_client or not voice_client.is_connected():
        return await interaction.response.send_message("Non sono in un canale vocale!", ephemeral=True)

    # Clear the guild's queue
    guild_id_str = str(interaction.guild_id)
    if guild_id_str in SONG_QUEUES:
        SONG_QUEUES[guild_id_str].clear()

    # If something is playing or paused, stop it
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    # I'm not completely sure why, but it disconnects without this, if it's not commented the bot throws an exception
    # (Optional) Disconnect from the channel
    # await voice_client.disconnect()

    await interaction.response.send_message("Ho fermato la riproduzione", ephemeral=True)


@bot.tree.command(name="play", description="Riproduci una canzone o aggiungila alla coda.")
@app_commands.describe(ricerca="Inserisci un URL o cerca la canzone")
async def play(interaction: discord.Interaction, ricerca: str):
    await interaction.response.defer(ephemeral=True)

    try:
        voice_channel = interaction.user.voice.channel
    except AttributeError:
        voice_channel = None

    if voice_channel is None:
        await interaction.followup.send("Devi essere in un canale vocale!", ephemeral=True)
        return

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)

    ydl_options = {
        "format": "bestaudio[abr<=128]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
        "format_sort": ["abr", "asr"], # this (somehow) serves as a fallback in case there are no formats that indicate the abr
    }

    if ricerca.startswith("https://youtube.com/") or ricerca.startswith("https://youtu.be/") or ricerca.startswith(
            "https://music.youtube.com/") or ricerca.startswith("https://www.youtu.be/") or ricerca.startswith(
        "https://www.youtube.com/"):
        url = sf.get_video_url(sf.get_video_id(ricerca))
        results = await search_ytdlp_async(url, ydl_options)
        audio_url = results["url"]
        title = results.get("title", "Untitled")

    else:
        query = "ytsearch1: " + ricerca
        results = await search_ytdlp_async(query, ydl_options)
        tracks = results.get("entries", [])

        if tracks is None:
            await interaction.followup.send("Nessun risultato trovato!", ephemeral=True)
            return

        first_track = tracks[0]
        audio_url = first_track["url"]
        print("THE AUDIO URL" + audio_url)
        title = first_track.get("title", "Untitled")

    guild_id = str(interaction.guild_id)
    if SONG_QUEUES.get(guild_id) is None:
        SONG_QUEUES[guild_id] = deque()

    SONG_QUEUES[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Aggiunto alla coda: **{title}**", ephemeral=True)
    else:
        await interaction.followup.send(f"Riproduco: **{title}**", ephemeral=True)
        await play_next_song(voice_client, guild_id, interaction.channel)


async def play_next_song(voice_client, guild_id, channel):
    if SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id][0]

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 128k",
        }

        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options)

        def after_play(error):
            if error:
                print(f"Whoops! Non sono riuscita a riprodurre {title}: {error}")

            if len(SONG_QUEUES[guild_id]) > 0:
                SONG_QUEUES[guild_id].popleft()

            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        voice_client.play(source, after=after_play)
        # asyncio.create_task(channel.send(f"Now playing: **{title}**"))
    else:
        await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()


bot.run(TOKEN)
