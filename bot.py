import os
import random
import discord
from discord.ext import commands

# ---------- INTENTS ----------
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
# WAŻNE: żeby komendy prefixowe (!teams) działały
intents.message_content = True

# ---------- BOT ----------
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")


@bot.command()
async def teams(ctx):
    # Użytkownik nie jest na kanale głosowym
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

    embed = discord.Embed(title="🎲 Wylosowane drużyny", color=0x00FF99)
    embed.add_field(
        name="🔵 Drużyna 1",
        value="\n".join(m.display_name for m in team1) or "Brak"
    )
    embed.add_field(
        name="🔴 Drużyna 2",
        value="\n".join(m.display_name for m in team2) or "Brak"
    )

    await ctx.send(embed=embed)


# ---------- TOKEN ----------
token = os.getenv("DISCORD_TOKEN")
print("DISCORD_TOKEN z env:", "USTAWIONY" if token else "BRAK!")  # debug w logach

if not token:
    # Tu celowo rzucamy bardziej czytelny błąd
    raise RuntimeError(
        "Zmienna środowiskowa DISCORD_TOKEN nie jest ustawiona. "
        "Upewnij się, że dodałeś ją w Railway -> Service -> Variables."
    )

bot.run(token)
