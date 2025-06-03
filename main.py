import os
import yt_dlp
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')

@bot.tree.command(name="konami", description="You forgot the Konami Code, didnt you?")
async def konami(interaction: discord.Interaction):
    await interaction.response.send_message("Konami Code: :arrow_up: :arrow_up: :arrow_down: :arrow_down: :arrow_left: :arrow_right: :arrow_left: :arrow_right: :regional_indicator_b: :regional_indicator_a:", ephemeral=True)

bot.run(TOKEN)