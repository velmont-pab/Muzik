import os
import shutil

import dotenv
import yt_dlp

dotenv.load_dotenv()
FFMPEG_PATH = os.getenv("FFMPEG_PATH")


def mostrar_progreso(d):
    if d["status"] == "downloading":
        porcentaje = d.get("_percent_str", "0%")
        velocidad = d.get("_speed_str", "Desconocida")
        eta = d.get("_eta_str", "Desconocido")

        print(
            f"\rDescargando: {porcentaje} | "
            f"Velocidad: {velocidad} | "
            f"Tiempo restante: {eta}",
            end="",
            flush=True)
        
    elif d["status"] == "finished":
        print("\nDescarga completada. Procesando audio...")


# -----------------------------
# COMPROBAR DENO
# -----------------------------
deno = shutil.which("deno")

if deno:
    print(f"Deno encontrado: {deno}")
else:
    print("Deno no fue encontrado.")


# -----------------------------
# PEDIR URL
# -----------------------------
while True:
    try:
        url = input("\nIngrese la URL del video: ").strip()
        if not url:
            print("La URL no puede estar vacía.")
            continue
        break
    except EOFError:
        print("\nNo se pudo leer la URL.")


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
    # -----------------------------5
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


    # -----------------------------
    # CONFIGURACIÓN DE DESCARGA
    # -----------------------------
    ydl_opts = {
        "format": "bestaudio/best",
        "ffmpeg_location":FFMPEG_PATH ,
        "outtmpl":
            os.path.join(carpeta_destino, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "progress_hooks": [mostrar_progreso],
    }


    # -----------------------------
    # DESCARGAR
    # -----------------------------
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n\n¡Descarga completa! 🎵")
    print(f"Guardado en: {carpeta_destino}")


except yt_dlp.utils.DownloadError as error:
    print(f"\nError durante la descarga: {error}")


except OSError as error:
    print(f"\nError del sistema: {error}")

