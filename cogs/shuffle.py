import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh


class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="shuffle", description="Attiva/disattiva lo shuffle")
    async def shuffle(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        await interaction.response.defer(ephemeral=True)

        # Check if the bot is in a voice channel
        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send("Non sono in un canale vocale!", ephemeral=True)

        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        if str(interaction.guild_id) in sh.LOOPED_QUEUES:
            return await interaction.followup.send("Shuffle e loop non sono compatibili!")

        if str(interaction.guild_id) not in sh.SHUFFLED_QUEUES:
            sh.SHUFFLED_QUEUES.append(str(interaction.guild_id))
            await interaction.followup.send("Shuffle attivato!", ephemeral=True)

        elif str(interaction.guild_id) in sh.SHUFFLED_QUEUES:
            sh.SHUFFLED_QUEUES.remove(str(interaction.guild_id))
            await interaction.followup.send("Shuffle disattivato!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Shuffle(bot))
