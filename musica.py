import os
import shutil

import dotenv
import yt_dlp

dotenv.load_dotenv()
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

def clear_screen():
    # 'nt' means Windows. Otherwise, it assumes Linux/Mac (POSIX)
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_progreso(d):
    if d["status"] == "downloading":
        porcentaje = d.get("_percent_str", "0%")
        velocidad = d.get("_speed_str", "Desconocida")
        eta = d.get("_eta_str", "Desconocido")
        print(
            f"\rDescargando: {porcentaje} | "
            f"Velocidad: {velocidad} | "
            f"Tiempo restante: {eta}",
            end=""
        )

    elif d["status"] == "finished":
        print("\nDescarga completada. Procesando audio...")


# Comprobar si Deno está disponible
print("Deno:", shutil.which("deno"))
clear_screen()
while True:
    try:
        url = input("Ingrese la URL del video: ")
        if not url:
            print("La URL no puede estar vacía. Por favor, ingrese una URL válida.")
            continue
        break

    except EOFError as error:
        print(f"A ocurrido un error: {error}. Ingrese una URL válida.")


# -----------------------------
# CONFIGURACIÓN PARA OBTENER
# INFORMACIÓN DEL VIDEO
# -----------------------------
info_opts = {"quiet": True}


try:
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        # Obtener información sin descargar
        info = ydl.extract_info(url, download=False)


    # -----------------------------
    # OBTENER AUTOR / ARTISTA
    # -----------------------------
    artista = (
        info.get("artist")
        or info.get("uploader")
        or info.get("channel")
        or "Artista desconocido"
    )


    # Obtener título
    titulo = info.get("title", "Cancion sin titulo")
    print("\nInformación encontrada:")
    print(f"Artista: {artista}")
    print(f"Título: {titulo}")


    # -----------------------------
    # CREAR CARPETA
    # -----------------------------
    carpeta_destino = os.path.join("Musik", artista)
    os.makedirs(carpeta_destino, exist_ok=True)

except yt_dlp.utils.DownloadError as error:
    print(f"\nError durante la descarga: {error}")

except OSError as error:
    print(f"\nError del sistema: {error}")


ydl_opts = {
    "format": "bestaudio/best",
    "ffmpeg_location": FFMPEG_PATH,
    "outtmpl": "%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }
    ],
    "progress_hooks": [mostrar_progreso],
}


try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("\nDescarga completa! 🎵")


except (yt_dlp.utils.DownloadError, OSError) as error:
    print(f"\nA ocurrido un error: {error}")