import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from gtts import gTTS
import requests
import asyncio
import yt_dlp
from collections import deque

# ---------- CARGAR TOKEN ----------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------- CONFIG BOT ----------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
FFMPEG_PATH = "C:/Users/Admin/Downloads/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"

# ---------- COLA DE REPRODUCCIÓN ----------
queue = deque()
is_playing = False

# ---------- FUNCIONES CLIMA ----------
def get_weather(city: str) -> str:
    base_url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(base_url)
    return response.text.strip() if response.status_code == 200 else "No se puede obtener la información solicitada"

# ---------- FUNCIONES TTS ----------
async def speak(voice_client, texto: str):
    tts = gTTS(text=texto, lang='es')
    tts.save("temp.mp3")
    source = discord.FFmpegPCMAudio("temp.mp3", executable=FFMPEG_PATH)
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(0.1)
    os.remove("temp.mp3")

# ---------- FUNCIONES MUSICALES ----------
async def get_youtube_audio(query: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info['url']

async def play_queue(ctx):
    global is_playing
    if is_playing or not queue:
        return

    is_playing = True
    while queue:
        song = queue.popleft()
        if os.path.isfile(song):  # Archivo local (MP3 subido)
            source = discord.FFmpegPCMAudio(song, executable=FFMPEG_PATH)
            ctx.voice_client.play(source)
        else:  # YouTube o búsqueda
            url = await get_youtube_audio(song)
            source = discord.FFmpegPCMAudio(url, executable=FFMPEG_PATH)
            ctx.voice_client.play(source)

        while ctx.voice_client.is_playing():
            await asyncio.sleep(0.5)
    is_playing = False

# ---------- COMANDOS VOZ ----------
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

# ---------- COMANDOS TTS ----------
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

# ---------- COMANDOS MÚSICA ----------
@bot.command()
async def play(ctx, *, query: str = None):
    """Agrega canción a la cola y reproduce (YouTube o MP3 subido)"""
    if not ctx.voice_client:
        await ctx.send("Primero debo unirme a un canal de voz con !entrar")
        return

    # Archivos MP3 subidos
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith(".mp3"):
                os.makedirs("downloads", exist_ok=True)
                file_path = f"downloads/{attachment.filename}"
                await attachment.save(file_path)
                queue.append(file_path)
                await ctx.send(f"🎵 Archivo agregado a la cola: {attachment.filename}")
    elif query:
        queue.append(query)
        await ctx.send(f"🎵 Agregado a la cola: {query}")
    else:
        await ctx.send("Debes escribir una búsqueda o subir un archivo .mp3")
        return

    await play_queue(ctx)

@bot.command()
async def cola(ctx):
    if queue:
        await ctx.send("🎶 Cola actual:\n" + "\n".join(queue))
    else:
        await ctx.send("La cola está vacía.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Música pausada.")
    else:
        await ctx.send("❌ No hay nada reproduciéndose.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Música reanudada.")
    else:
        await ctx.send("❌ No hay nada en pausa.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Canción saltada.")
    else:
        await ctx.send("❌ No hay nada sonando.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        queue.clear()  # Limpiar cola
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Música detenida y cola vacía.")
    else:
        await ctx.send("❌ No estoy en un canal de voz.")

# ---------- INICIAR BOT ----------
bot.run(TOKEN)












