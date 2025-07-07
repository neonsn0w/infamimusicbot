import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh


class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="loop", description="Attiva/Disattiva il loop la canzone attuale")
    async def loop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        await interaction.response.defer(ephemeral=True)

        # Check if the bot is in a voice channel
        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send("Non sono in un canale vocale!", ephemeral=True)

        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        if str(interaction.guild_id) in sh.SHUFFLED_QUEUES:
            return await interaction.followup.send("Shuffle e loop non sono compatibili!")

        if str(interaction.guild_id) in sh.LOOPED_QUEUES:
            sh.LOOPED_QUEUES.remove(str(interaction.guild_id))
            return await interaction.followup.send("Disattivato il loop")

        if str(interaction.guild_id) not in sh.LOOPED_QUEUES:
            sh.LOOPED_QUEUES.append(str(interaction.guild_id))
            return await interaction.followup.send("Attivato il loop")

async def setup(bot):
    await bot.add_cog(Loop(bot))