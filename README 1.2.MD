1. Detectamos si es una playlist

La parte clave es:
    
    entries = info.get("entries")

Para un video individual:
    
    entries = None

Para una playlist:

    entries = [
        cancion1,
        cancion2,
        cancion3
    ]

Entonces:

    if entries:

significa:
Si existen canciones dentro de entries, procesamos una playlist.


2.Creamos una lista limpia

    canciones = [
        cancion
        for cancion in entries
        if cancion is not None
    ]

Esto es una comprensión de listas.
Es equivalente a:

    canciones = []

    for cancion in entries:

        if cancion is not None:

            canciones.append(cancion)

Lo hacemos para evitar problemas si algún elemento de la playlist viene vacío.


3. Seleccionamos un rango

Si la playlist tiene:

    1 - Canción A
    2 - Canción B
    3 - Canción C
    4 - Canción D
    5 - Canción E

Y eliges:

    Desde: 2
    Hasta: 4

Python utiliza:

    seleccionadas = canciones[inicio - 1:fin]

El resultado será:

    Canción B
    Canción C
    Canción D

Restamos uno al inicio porque las listas de Python comienzan en:

    0

pero nosotros queremos que el usuario vea:

    1

4. Cada canción obtiene su propia carpeta

Esta es la diferencia más importante respecto al código anterior:

    for numero, cancion in enumerate(seleccionadas, start=inicio):

Ahora procesamos cada canción individualmente.

Para cada una hacemos:

    artista = obtener_artista(cancion)

Y después:

    carpeta_destino = os.path.join(
        "Musica",
        artista
    )

Por eso una playlist con varios artistas termina organizada así:

    Musica/
    │
    ├── Queen/
    │   └── Radio Ga Ga.mp3
    │
    ├── Bon Jovi/
    │   └── Livin' on a Prayer.mp3
    │
    └── Europe/
        └── The Final Countdown.mp3


Hay una mejora importante que haría ahora

El código funciona como base de aprendizaje, pero tiene una limitación: repite mucho la configuración de descarga.

Por ejemplo, este bloque aparece prácticamente dos veces:

    ydl_opts = {
        "format": "bestaudio/best",
        ...
    }


