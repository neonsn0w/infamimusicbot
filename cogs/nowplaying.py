import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh
from utils.song import Song


class Nowplaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="nowplaying", description="Controlla che canzone è in riproduzione.")
    async def nowplaying(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)

        if interaction.guild.voice_client is None or guild_id not in sh.SONG_QUEUES or not sh.SONG_QUEUES[guild_id]:
            return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

        song = sh.SONG_QUEUES[guild_id][0]
        await interaction.response.send_message(
            f"Sto riproducendo: **[{song.title}]({song.url})**", ephemeral=True
    )


async def setup(bot):
    await bot.add_cog(Nowplaying(bot))
