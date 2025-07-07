import discord
from discord.ext import commands
from discord import app_commands


class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="resume", description="Riprendi la riproduzione messa in pausa.")
    async def resume(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        await interaction.response.defer(ephemeral=True)
        # Check if the bot is in a voice channel
        if voice_client is None:
            return await interaction.followup.send("Non sono in un canale vocale!", ephemeral=True)

        # Check if it's actually paused
        if not voice_client.is_paused():
            return await interaction.followup.send("La riproduzione non è in pausa!", ephemeral=True)

        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        # Resume playback
        voice_client.resume()
        await interaction.followup.send("Riprendo la riproduzione", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Resume(bot))