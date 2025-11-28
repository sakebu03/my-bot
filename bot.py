import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True   # <-- DODANE
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")      # prosta komenda testowa

@bot.command()
async def teams(ctx):
    if ctx.author.voice is None:
        await ctx.send("Musisz być na kanale głosowym, żeby losować drużyny!")
        return

    channel = ctx.author.voice.channel
    members = [m for m in channel.members if not m.bot]

    if len(members) < 2:
        await ctx.send("Za mało osób na kanale!")
        return

    random.shuffle(members)
    mid = len(members) // 2
    team1 = members[:mid]
    team2 = members[mid:]

    embed = discord.Embed(title="🎲 Wylosowane drużyny", color=0x00ff99)
    embed.add_field(name="🔵 Drużyna 1", value="\n".join(m.display_name for m in team1))
    embed.add_field(name="🔴 Drużyna 2", value="\n".join(m.display_name for m in team2))

    await ctx.send(embed=embed)

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError(
        "Brak zmiennej środowiskowej DISCORD_TOKEN.\n"
        "Na Railway ustaw nazwę: DISCORD_TOKEN, wartość: BOT TOKEN z zakładki Bot w Discord Developer Portal."
    )

bot.run(token)
