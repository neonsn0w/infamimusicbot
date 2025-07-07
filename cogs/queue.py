import discord
from discord.ext import commands
from discord import app_commands

from utils import shared as sh
from utils.song import Song


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="queue", description="Visualizza la coda di riproduzione.")
    async def queue(self, interaction: discord.Interaction):
        if interaction.guild.voice_client is None or len(sh.SONG_QUEUES) == 0 or len(
                sh.SONG_QUEUES[str(interaction.guild_id)]) == 0:
            return await interaction.response.send_message("Non sto riproducendo nulla!", ephemeral=True)

        queue_msg: str = "Ecco la coda:\n\n"

        for i, song in enumerate(sh.SONG_QUEUES[str(interaction.guild_id)]):
            if i == 0:
                queue_msg += f"**IN RIPRODUZIONE: [{song.title}](<{song.url}>)**\n"
            else:
                queue_msg += f"{str(i)}. **[{song.title}](<{song.url}>)**\n"
        if str(interaction.guild_id) in sh.SHUFFLED_QUEUES:
            queue_msg += "\n🔀 QUEUE IN SHUFFLE 🔀"
        if str(interaction.guild_id) in sh.LOOPED_QUEUES:
            queue_msg += "\n🔁 QUEUE IN LOOP 🔁"

        await interaction.response.send_message(queue_msg, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Queue(bot))
