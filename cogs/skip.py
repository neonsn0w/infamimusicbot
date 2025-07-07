import discord
from discord.ext import commands
from discord import app_commands


class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="skip", description="Salta la canzone in riproduzione")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        voice_client = interaction.guild.voice_client
        if not interaction.user.voice or interaction.user.voice.channel.id != voice_client.channel.id:
            return await interaction.followup.send("Devi essere nel mio canale vocale!", ephemeral=True)

        if interaction.guild.voice_client and (
                interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
            interaction.guild.voice_client.stop()
            await interaction.followup.send("Canzone saltata.", ephemeral=True)
        else:
            await interaction.followup.send("Non sto riproducendo nulla!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Skip(bot))
