import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="remove", description="Rimuovi una canzone")
    async def remove(self, interaction: discord.Interaction, indice: int):
        voice_client = interaction.guild.voice_client
        await interaction.response.defer(ephemeral=True)
        if len(sh.SONG_QUEUES[str(interaction.guild.id)]) == 0:
            return await interaction.followup.send("Non sto riproducendo nulla!", ephemeral=True)
        elif indice > len(sh.SONG_QUEUES[str(interaction.guild.id)]):
            return await interaction.followup.send("Questa canzone non esiste!", ephemeral=True)

        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        if indice <= 0:
            # you know what you did...
            return await interaction.followup.send(
                "https://tenor.com/view/miku-angry-meme-goku-angry-miku-meme-meme-hatsune-miku-gif-5683637212704483663",
                ephemeral=True)
            # return await interaction.followup.send("Inserire un indice maggiore di 0", ephemeral=True)

        else:
            nomecanzone = sh.SONG_QUEUES[str(interaction.guild_id)][indice][1]
            sh.SONG_QUEUES[str(interaction.guild_id)].remove(sh.SONG_QUEUES[str(interaction.guild_id)][indice])
            return await interaction.followup.send(f"{nomecanzone} è stata rimossa", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Remove(bot))