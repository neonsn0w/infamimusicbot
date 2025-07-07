import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="stop", description="Ferma la riproduzione.")
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        await interaction.response.defer(ephemeral=True)

        # Check if the bot is in a voice channel
        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send("Non sono in un canale vocale!", ephemeral=True)

        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        # Clear the guild's queue
        guild_id_str = str(interaction.guild_id)
        if guild_id_str in sh.SONG_QUEUES:
            sh.SONG_QUEUES[guild_id_str].clear()

        # Disables shuffle and loop after bot is stopped

        if guild_id_str in sh.SHUFFLED_QUEUES:
            sh.SHUFFLED_QUEUES.remove(guild_id_str)

        if guild_id_str in sh.LOOPED_QUEUES:
            sh.LOOPED_QUEUES.remove(guild_id_str)

        # If something is playing or paused, stop it
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()

        await interaction.followup.send("Ho fermato la riproduzione", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Stop(bot))
