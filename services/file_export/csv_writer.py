import csv
from models.entities import Noticia, Article
import os

def guardar_noticias_en_csv(noticias: list[Noticia], nombre_archivo: str = "noticias.csv"):
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
    print(f"✅ Archivo de noticias guardado como: {nombre_archivo}")


def guardar_articles_en_csv(articulos: list[Article], nombre_archivo: str = "articulos.csv"):
    """
    Guarda una lista de objetos Article en un archivo CSV.

    Parámetros:
    - articulos: Lista de objetos Article a guardar.
    - nombre_archivo: Nombre del archivo de salida. Por defecto "articulos.csv".

    Crea el archivo en la ruta actual con columnas dinámicas basadas en los atributos de Article.
    """
    if not articulos:
        print("⚠️ No hay artículos para guardar en el archivo CSV.")
        return

    # Obtener los nombres de los atributos de la clase Article
    columnas = [attr for attr in dir(articulos[0]) if not callable(getattr(articulos[0], attr)) and not attr.startswith("__")]

    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        
        # Escribir las cabeceras del archivo CSV
        writer.writerow(columnas)
        
        # Escribir los datos de cada artículo
        for articulo in articulos:
            writer.writerow([getattr(articulo, columna, "") for columna in columnas])
    
    print(f"✅ Archivo de artículos guardado como: {nombre_archivo}")


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
