import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh

import requests

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="lyrics", description="Cerca il testo della canzone in riproduzione.")
    async def lyrics(self, interaction: discord.Interaction):
        
        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.guild.voice_client is None or len(sh.SONG_QUEUES) == 0 or len(
                sh.SONG_QUEUES[str(interaction.guild_id)]) == 0:
                return await interaction.followup.send("Non sto riproducendo nulla!", ephemeral=True)
            elif not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
                return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)
        except Exception as e:
            print(e)
        req = requests.get(f'https://lrclib.net/api/search?q={sh.SONG_QUEUES[str(interaction.guild_id)][0][1]}')
        try:
            if len(req.json()) > 0:
                if not req.json()[0]['instrumental']:
                    return await interaction.followup.send(req.json()[0]['plainLyrics'], ephemeral = True)
                else:
                    return await interaction.followup.send('Questa canzone non ha testo!', ephemeral = True)
            else:
                return await interaction.followup.send('Non ho trovato il testo di questa canzone!', ephemeral = True)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Lyrics(bot))
