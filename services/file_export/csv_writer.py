import csv
from models.entities import Noticia

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
