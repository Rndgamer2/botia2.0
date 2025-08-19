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

# ARREGLO IMPORTANTE DEL BOT

El mensaje clave era este:

KeyError: 'url'


Eso significa que tu código intentaba acceder a info['url'] dentro de la función get_youtube_audio, pero esa clave no existía en el diccionario que devolvía yt_dlp.

¿Por qué ocurría?

Cuando usas 'default_search': 'ytsearch' en yt_dlp, si la búsqueda devuelve varios resultados, yt_dlp no devuelve directamente un diccionario con 'url'.

Devuelve un diccionario con una clave 'entries' que contiene la lista de resultados.

Cada resultado dentro de 'entries' sí tiene la URL que necesitas ('url' o 'webpage_url').

En tu código original hacías:

info = ydl.extract_info(query, download=False)
return info['url']


Esto funciona si query es un enlace directo de YouTube.

Pero si query era un término de búsqueda (por ejemplo: "Smack that"), info no tenía 'url', sino 'entries', y por eso saltaba el KeyError.

Cómo lo arreglamos

En mi versión corregida, agregamos:

if 'entries' in info and len(info['entries']) > 0:
    info = info['entries'][0]
return info['url'] if 'url' in info else info['webpage_url']


Esto hace dos cosas:

Si info contiene 'entries' (una búsqueda), toma el primer resultado.

Si no existe 'url', usamos 'webpage_url', que siempre apunta al video.