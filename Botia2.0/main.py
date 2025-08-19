import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
from gtts import gTTS
import asyncio

# ---------- CARGAR TOKEN ----------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------- CONFIG BOT ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- FUNCIONES CLIMA ----------
def get_weather(city: str) -> str:
    base_url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "No se puede obtener la información solicitada"

# ---------- FUNCIONES TTS ----------
FFMPEG_PATH = "C:/Users/Admin/Downloads/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"

async def speak(voice_client, texto: str):
    """Genera TTS con gTTS y lo reproduce en Discord usando FFmpeg"""
    tts = gTTS(text=texto, lang='es')
    tts.save("temp.mp3")  # Archivo temporal

    source = discord.FFmpegPCMAudio(
        source="temp.mp3",
        executable=FFMPEG_PATH
    )
    voice_client.play(source)

    # Espera a que termine de hablar
    while voice_client.is_playing():
        await asyncio.sleep(0.1)
    
    os.remove("temp.mp3")  # Borra el archivo temporal

# ---------- COMANDOS ----------
@bot.command()
async def entrar(ctx):
    if ctx.author.voice:
        canal = ctx.author.voice.channel
        await canal.connect()
        await ctx.send(f"Me uní a {canal}")
    else:
        await ctx.send("¡No estás en un canal de voz!")

@bot.command()
async def salir(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Me desconecté del canal de voz")
    else:
        await ctx.send("¡No estoy en un canal de voz!")

@bot.command()
async def say(ctx, *, mensaje: str):
    await ctx.send(f"📢 {mensaje}")
    if ctx.voice_client:
        await speak(ctx.voice_client, mensaje)

@bot.command()
async def weather(ctx, *, city: str):
    info = get_weather(city)
    texto = f"Clima en {city}: {info}"
    await ctx.send(texto)
    if ctx.voice_client:
        await speak(ctx.voice_client, texto)

# ---------- INICIAR BOT ----------
bot.run(TOKEN)











