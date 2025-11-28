import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # żeby !teams działało

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user} (ID: {bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def teams(ctx):
    if ctx.author.voice is None:
        await ctx.send("Musisz być na kanale głosowym, żeby losować drużyny!")
        return

    channel = ctx.author.voice.channel
    members = [m for m in channel.members if not m.bot]

    if len(members) < 2:
        await ctx.send("Za mało osób na kanale, potrzeba minimum 2!")
        return

    random.shuffle(members)
    mid = len(members) // 2
    team1 = members[:mid]
    team2 = members[mid:]

    embed = discord.Embed(title="🎲 Wylosowane drużyny", color=0x00ff99)
    embed.add_field(name="🔵 Drużyna 1", value="\n".join(m.display_name for m in team1) or "—")
    embed.add_field(name="🔴 Drużyna 2", value="\n".join(m.display_name for m in team2) or "—")

    await ctx.send(embed=embed)

# --- TOKEN Z ENV ---
token = os.getenv("DISCORD_TOKEN")

if not token:
    raise RuntimeError(
        "Brak zmiennej środowiskowej DISCORD_TOKEN.\n"
        "Na Railway ustaw nazwę: DISCORD_TOKEN, wartość: TWÓJ BOT TOKEN z zakładki Bot w Discord Developer Portal."
    )

bot.run(token)




