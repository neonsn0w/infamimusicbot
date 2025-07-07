import discord
from discord.ext import commands
from discord import app_commands


class Konami(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="konami", description="You forgot the Konami Code, didnt you?")
    async def konami(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Konami Code: :arrow_up: :arrow_up: :arrow_down: :arrow_down: :arrow_left: :arrow_right: :arrow_left: :arrow_right: :regional_indicator_b: :regional_indicator_a:",
            ephemeral=True)

async def setup(bot):
    await bot.add_cog(Konami(bot))