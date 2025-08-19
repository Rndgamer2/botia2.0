Botia2.0 – Discord Music & TTS Bot

Bot de Discord con funcionalidades de TTS, clima, y reproducción de música desde YouTube y archivos MP3 subidos.

⚙️ Instalación

Clona este repositorio o descarga el código.

Instala las dependencias:

pip install discord.py python-dotenv gTTS yt-dlp requests


Descarga FFmpeg
 y actualiza la ruta FFMPEG_PATH en main.py.

Crea un archivo .env con tu token de Discord:

DISCORD_TOKEN=TU_TOKEN_AQUI


Ejecuta el bot:

python main.py

🎶 Comandos del Bot
Voz

!entrar → El bot se une al canal de voz donde estás.

!salir → El bot se desconecta del canal de voz.

Texto a Voz (TTS)

!say <mensaje> → El bot repite tu mensaje en el canal de voz.

!weather <ciudad> → El bot dice el clima de la ciudad indicada.

Música

!play <URL o búsqueda> → Reproduce una canción de YouTube o agrega un archivo MP3 subido.

!cola → Muestra la cola de canciones.

!pause → Pausa la canción actual.

!resume → Reanuda la canción pausada.

!skip → Salta la canción actual y reproduce la siguiente en la cola.

!stop → Detiene la música, limpia la cola y desconecta el bot.

Archivos MP3

Sube un archivo .mp3 al canal y usa !play sin argumento.

Se agregará automáticamente a la cola de reproducción.

📌 Notas

Asegúrate de que FFmpeg esté instalado y la ruta correcta configurada en main.py.

El bot reproduce canciones en orden de llegada (cola FIFO).

Puedes combinar YouTube y archivos locales en la misma cola.