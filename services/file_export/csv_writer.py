import csv
from models.entities import Noticia
import os

def guardar_en_csv(noticias: list[Noticia], nombre_archivo: str = "noticias.csv"):
    """
    Guarda una lista de objetos Noticia en un archivo CSV.

    Parámetros:
    - noticias: Lista de objetos Noticia a guardar.
    - nombre_archivo: Nombre del archivo de salida. Por defecto "noticias.csv".

    Crea el archivo en la ruta actual con columnas: Título, Fecha, Descripción, URL, Fuente.
    """
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["Título", "Fecha", "Descripción", "URL", "Fuente"])
        for noticia in noticias:
            writer.writerow([
                noticia.titulo,
                noticia.fecha,
                noticia.descripcion,
                noticia.url,
                noticia.fuente
            ])
    print(f"✅ Archivo guardado como: {nombre_archivo}")

def leer_desde_csv(nombre_archivo: str) -> list[Noticia]:
    """
    Lee un archivo CSV y lo convierte en una lista de objetos Noticia.

    Parámetros:
    - nombre_archivo: Nombre del archivo CSV a leer.

    Retorna:
    - Una lista de objetos Noticia.
    """
    # Construir la ruta completa al archivo CSV
    ruta_csv = os.path.join(os.getcwd(), nombre_archivo)

    noticias = []
    with open(ruta_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            noticia = Noticia(
                titulo=row["Título"],
                fecha=row["Fecha"],
                descripcion=row["Descripción"],
                url=row["URL"],
                fuente=row["Fuente"]
            )
            noticias.append(noticia)
    print(f"✅ Archivo leído: {ruta_csv}")
    return noticias
