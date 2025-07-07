import discord
from discord.ext import commands
from discord import app_commands


class Dementia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__.lower()} command loaded from {__file__}')

    @app_commands.command(name="dementia", description="i forgor.")
    async def dementia(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "https://cdn.discordapp.com/attachments/484399910280757250/1380274678379184239/dementia.mp4?ex=68434877&is=6841f6f7&hm=79d3325914cac39de0aca7c575fc44edc8581f482c88855133169bb5c2c2397b&",
            ephemeral=True)


async def setup(bot):
    await bot.add_cog(Dementia(bot))
