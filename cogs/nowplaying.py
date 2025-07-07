import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh
from utils.shared import is_playing, get_current_song

class Nowplaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="nowplaying", description="Controlla che canzone è in riproduzione.")
    async def nowplaying(self, interaction: discord.Interaction):
        if not is_playing(interaction.guild):
            return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

        current = get_current_song(interaction.guild_id)
        title, url = current[1], current[2]

        await interaction.response.send_message(
            f"Sto riproducendo: **[{title}]({url})**",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Nowplaying(bot))
