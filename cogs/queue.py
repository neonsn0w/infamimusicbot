import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh
from utils.shared import is_playing, get_queue


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="queue", description="Visualizza la coda di riproduzione.")
    async def queue(self, interaction: discord.Interaction):
        if not is_playing(interaction.guild):
            return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

        queue = get_queue(interaction.guild_id)
        queue_msg = "Ecco la coda:\n\n"

        for i, song in enumerate(queue):
            line = f"**[{song[1]}](<{song[2]}>)**"
            queue_msg += f"**IN RIPRODUZIONE: {line}**\n" if i == 0 else f"{i}. {line}\n"

        if str(interaction.guild_id) in sh.SHUFFLED_QUEUES:
            queue_msg += "\n🔀 QUEUE IN SHUFFLE 🔀"
        if str(interaction.guild_id) in sh.LOOPED_QUEUES:
            queue_msg += "\n🔁 QUEUE IN LOOP 🔁"

        await interaction.response.send_message(queue_msg, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Queue(bot))
