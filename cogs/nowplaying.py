import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh


class Nowplaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="nowplaying", description="Controlla che canzone è in riproduzione.")
    async def nowplaying(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None or len(sh.SONG_QUEUES) == 0 or len(
                sh.SONG_QUEUES[str(interaction.guild_id)]) == 0:
            return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

        await interaction.response.send_message(
            f"Sto riproducendo: **[{sh.SONG_QUEUES[str(interaction.guild_id)][0][1]}]({sh.SONG_QUEUES[str(interaction.guild_id)][0][2]})**",
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(Nowplaying(bot))
