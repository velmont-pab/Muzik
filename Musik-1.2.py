import os
import re
import shutil

import dotenv
import yt_dlp

dotenv.load_dotenv()

FFMPEG_PATH = os.getenv("FFMPEG_PATH")


# ==========================================
# LIMPIAR NOMBRES PARA WINDOWS
# ==========================================
def limpiar_nombre(nombre):
    caracteres_invalidos = r'[\\"/:*?"<>|]'
    nombre = re.sub(caracteres_invalidos, "-", nombre)
    return nombre.strip()


# ==========================================
# MOSTRAR PROGRESO
# ==========================================
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
            flush=True,
        )

    elif d["status"] == "finished":
        print("\nDescarga completada. Procesando audio...")


# ==========================================
# OBTENER ARTISTA
# ==========================================
def obtener_artista(info):
    artista = (
        info.get("artist")
        or info.get("uploader")
        or info.get("channel")
        or "Artista desconocido"
    )
    return limpiar_nombre(artista)


# ==========================================
# COMPROBAR DENO
# ==========================================
deno = shutil.which("deno")
if deno:
    print(f"Deno encontrado: {deno}")
else:
    print("Deno no fue encontrado.")


# ==========================================
# PEDIR URL
# ==========================================
while True:
    try:
        url = input("\nIngrese la URL del video o playlist: ").strip()

        if not url:
            print("La URL no puede estar vacía.")
            continue
        break

    except EOFError:
        print("\nNo se pudo leer la URL.")


# ==========================================
# OBTENER INFORMACIÓN
# ==========================================
info_opts = {"quiet": True, "extract_flat": False}


try:
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # ==========================================
    # DETECTAR PLAYLIST
    # ==========================================
    entries = info.get("entries")
    if entries:
        print("\n📃 Playlist encontrada")
        nombre_playlist = info.get("title", "Playlist sin nombre")
        print(f"Nombre: {nombre_playlist}")
        canciones = [cancion for cancion in entries if cancion is not None]
        print(f"Cantidad de canciones: {len(canciones)}")


        # ==========================================
        # ELEGIR QUÉ DESCARGAR
        # ==========================================
        print("\n¿Qué desea hacer?")
        print("1 - Descargar toda la playlist")
        print("2 - Descargar un rango de canciones")
        print("3 - Cancelar")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            inicio = 1
            fin = len(canciones)

        elif opcion == "2":
            while True:
                try:
                    inicio = int(input("Descargar desde la canción número: "))
                    fin = int(input("Hasta la canción número: "))

                    if inicio < 1 or fin > len(canciones):
                        print("El rango está fuera de los límites.")
                        continue

                    if inicio > fin:
                        print("El inicio no puede ser mayor al final.")
                        continue
                    break

                except ValueError:
                    print("Ingrese números válidos.")

        elif opcion == "3":
            print("\nDescarga cancelada.")
            raise SystemExit

        else:
            print("\nOpción no válida.")
            raise SystemExit

        # ==========================================
        # PROCESAR CANCIONES
        # ==========================================
        seleccionadas = canciones[inicio - 1 : fin]
        print(f"\nSe descargarán {len(seleccionadas)} canciones.\n")

        for numero, cancion in enumerate(seleccionadas, start=inicio):
            titulo = cancion.get("title", "Cancion sin titulo")
            artista = obtener_artista(cancion)
            print(f"\n[{numero}/{fin}] {artista} - {titulo}")

            carpeta_destino = os.path.join("Musik", artista)
            os.makedirs(carpeta_destino, exist_ok=True)

            ydl_opts = {
                "format": "bestaudio/best",
                "ffmpeg_location": FFMPEG_PATH,#THE LOCAL PATH OF FFMPEG 
                "outtmpl": os.path.join(carpeta_destino, "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                    }
                ],
                "progress_hooks": [mostrar_progreso],
                # Descargar solo este video
                "noplaylist": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([cancion["webpage_url"]])

            except yt_dlp.utils.DownloadError as error:
                print(f"\nError descargando {titulo}: {error}")

        print("\n\n🎵 ¡Playlist descargada!")

    # ==========================================
    # VIDEO INDIVIDUAL
    # ==========================================

    else:
        print("\n🎵 Video individual encontrado")
        artista = obtener_artista(info)

        titulo = info.get("title", "Cancion sin titulo")
        print(f"Artista: {artista}")
        print(f"Título: {titulo}")

        carpeta_destino = os.path.join("Musik", artista)
        os.makedirs(carpeta_destino, exist_ok=True)

        ydl_opts = {
            "format": "bestaudio/best",
            "ffmpeg_location": FFMPEG_PATH,#THE LOCAL PATH OF FFMPEG
            "outtmpl": os.path.join(carpeta_destino, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
            "progress_hooks": [mostrar_progreso],
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("\n\n🎵 ¡Descarga completa!")


except yt_dlp.utils.DownloadError as error:
    print(f"\nError durante la descarga: {error}")


except OSError as error:
    print(f"\nError del sistema: {error}")
