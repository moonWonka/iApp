import pytz
from datetime import datetime
from models.entities import Article, Noticia
from repository.article_repository import insert_article, get_articles_by_processed_status
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export import guardar_en_csv, leer_desde_csv


# Constante para la zona horaria de América/Santiago
TZ_SANTIAGO = pytz.timezone("America/Santiago")

def load_data_to_db():
    # Obtener la fecha y hora actual en la zona horaria de Santiago
    fecha_hora_actual = datetime.now(TZ_SANTIAGO)
    print(f"Fecha y hora actual en Santiago: {fecha_hora_actual}")

    # Carga de datos a DB desde csv
    diario_a: list[Noticia] = leer_desde_csv("noticias.csv")
    diario_b: list[Noticia] = leer_desde_csv("noticias2.csv")

    # Combinar ambas listas en una sola (todas las fuentes)
    diarios_data: list[Noticia] = diario_a + diario_b

    print("Cargando datos desde los archivos CSV... 📂")

    for noticia in diarios_data:
        print(f"Procesando noticia: {noticia.titulo}")

        # Crear el objeto Noticia
        nueva_noticia = Noticia(
            titulo=noticia.titulo,
            fecha=fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            descripcion=noticia.descripcion,
            url=noticia.url,
            fuente=noticia.fuente
        )

        # Insertar la noticia en la base de datos
        insert_article(nueva_noticia)

    print("Inserción de datos completada con éxito 🚀")

def get_data_from_db() -> list[Article]:
    """
    Obtiene artículos no procesados desde la base de datos y los imprime.

    Retorna:
    - Una lista de objetos Article que no han sido procesados (IS_PROCESSED = False).
    """
    try:
        # Obtener artículos no procesados
        articulos: list[Article] = get_articles_by_processed_status(processed_status=False)

        if not articulos:
            print("⚠️ No se encontraron artículos no procesados en la base de datos.")
            return []

        print(f"✅ Se encontraron {len(articulos)} artículos no procesados:")
        for articulo in articulos:
            print(f"- ID: {articulo.id}, Título: {articulo.titulo}, Fecha: {articulo.fecha}")

        return articulos

    except Exception as e:
        print(f"❌ Error al obtener datos de la base de datos: {e}")
        return []


def procesar_datos() -> None:
    """
    Función principal para procesar datos desde periódicos y realizar operaciones en la base de datos.
    """
    # Obtener información de periódicos
    #datos_diario_a: list[Noticia] = extraer_noticias_araucaniadiario(max_articulos=100)
    #datos_diario_b: list[Noticia] = extraer_noticias_elperiodico(max_articulos=100)

    #guardar informacion en csv
    #guardar_en_csv(datos_diario_a)
    #guardar_en_csv(datos_diario_b, nombre_archivo="noticias2.csv")

    # carga informacion hacia DB
    #load_data_to_db()

    # Obtener datos de DB
    get_data_from_db()
    
    # Procesa Data con modelos de IA

    # Revisar datos de DB no procesados
    # ...

    # Enviar datos a API para procesar la data
    # ...

    # Obtener datos de API
    # ...

