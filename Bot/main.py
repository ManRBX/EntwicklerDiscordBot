import discord
from discord.ext import commands
import asyncio
import config  # Importiert die Token-Datei

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'✅ Bot ist online als {bot.user}')

# Lade Cogs (Admin- und Help-Commands)
async def load_cogs():
    await bot.load_extension("admin_commands")
    await bot.load_extension("help_command")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.BOT_TOKEN)  # Token aus config.py laden

asyncio.run(main())