import os
import yt_dlp
import discord
from discord.ext import commands
from discord import app_commands, http
from dotenv import load_dotenv
from collections import deque
import asyncio
import random

from utils import string_functions as sf
from utils import shared as sh
from utils.song import Song

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


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
    print(f'{bot.user} has connected to Discord! :3')


@bot.tree.command(name="play", description="Riproduci una canzone o aggiungila alla coda.")
@app_commands.describe(ricerca="Inserisci un URL o cerca la canzone")
async def play(interaction: discord.Interaction, ricerca: str):
    await interaction.response.defer(ephemeral=True)

    try: 
        voice_channel = interaction.user.voice.channel
    except AttributeError:
        return await interaction.followup.send("Devi essere in un canale vocale!", ephemeral=True)

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)

    ydl_options = {
        "format": "bestaudio",
        "noplaylist": True,
    }

    if any(ricerca.startswith(prefix) for prefix in ( # url diretto
        "https://youtube.com/", "https://youtu.be/", "https://music.youtube.com/",
        "https://www.youtu.be/", "https://www.youtube.com/"
    )):

        url = sf.get_video_url(sf.get_video_id(ricerca))
        results = await search_ytdlp_async(sf.get_video_url(sf.get_video_id(ricerca)), ydl_options)

        audio_url = results["url"]
        title = results.get("title", "Untitled")

    else: # ricerca
        results = await search_ytdlp_async(f"ytsearch1:{ricerca}", ydl_options)

        if not results or 'entries' not in results or not results['entries']:
            return None, None

        first_entry = results['entries'][0]

        url = sf.get_video_url(first_entry['id'])
        video_info = await search_ytdlp_async(url, ydl_options)

        audio_url = video_info['url']
        title = first_entry.get('title', video_info.get('title', 'Untitled'))

    guild_id = str(interaction.guild_id)

    if sh.SONG_QUEUES.get(guild_id) is None:
        sh.SONG_QUEUES[guild_id] = deque()

    sh.SONG_QUEUES[guild_id].append(Song(audio_url, title, url))

    if voice_client.is_playing() or voice_client.is_paused():
        await interaction.followup.send(f"Aggiunto alla coda: **[{title}]({url})**", ephemeral=True)
    else:
        await interaction.followup.send(f"Riproduco: **[{title}]({url})**", ephemeral=True)
        await play_next_song(voice_client, guild_id, interaction.channel)



async def play_next_song(voice_client, guild_id, channel):
    if sh.SONG_QUEUES[guild_id]:
        if len(sh.SONG_QUEUES[guild_id]) > 2:
            randsong = random.randint(1, len(sh.SONG_QUEUES[guild_id]) - 1)
        if guild_id not in sh.SHUFFLED_QUEUES:
            song = sh.SONG_QUEUES[guild_id][0]
        elif guild_id in sh.SHUFFLED_QUEUES:
            song = sh.SONG_QUEUES[guild_id][randsong]

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 128k",
        }

        if len(sh.SONG_QUEUES[guild_id]) > 2 and guild_id in sh.SHUFFLED_QUEUES:
            sh.SONG_QUEUES[guild_id].appendleft(song)

        source = discord.FFmpegOpusAudio(song.audio_url, **ffmpeg_options)

        try:
            await bot.http.edit_voice_channel_status(status=title, channel_id=voice_client.channel.id)
        except Exception as e:
            print(e)

        def after_play(error):
            if error:
                print(f"Whoops! Non sono riuscita a riprodurre {song.title}: {error}")

            if guild_id not in sh.LOOPED_QUEUES and len(sh.SONG_QUEUES[guild_id]) > 0:
                sh.SONG_QUEUES[guild_id].popleft()

            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), bot.loop)

        voice_client.play(source, after=after_play)
        # asyncio.create_task(channel.send(f"Now playing: **{title}**"))
    else:
        try:
            await bot.http.edit_voice_channel_status(status=None, channel_id=voice_client.channel.id)
        except Exception as e:
            print(e)
        await voice_client.disconnect()
        sh.SONG_QUEUES[guild_id] = deque()



async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
