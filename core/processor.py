import pytz
from datetime import datetime
from models.entities import Noticia
from repository.article_repository import insert_article
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export import guardar_en_csv, leer_desde_csv


# Constante para la zona horaria de América/Santiago
TZ_SANTIAGO = pytz.timezone("America/Santiago")

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

    # Obtener la fecha y hora actual en la zona horaria de Santiago
    fecha_hora_actual = datetime.now(TZ_SANTIAGO)
    print(f"Fecha y hora actual en Santiago: {fecha_hora_actual}")

    # Carga de datos a DB desde csv
    diario_a: list[Noticia] = leer_desde_csv("noticias.csv")
    diario_b: list[Noticia] = leer_desde_csv("noticias2.csv")

    # Combinar ambas listas en una sola(todas las fuentes)
    diarios_data: list[Noticia] = diario_a + diario_b

    print("datosss! 👌👌")
    for noticia in diarios_data:
        print(noticia.titulo)
        insert_article(
            title=noticia.titulo,
            date=fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            url=noticia.url,
            source=noticia.fuente,
            description=noticia.descripcion
        )
    
    print("insersion de datas exitosa 🚀🚀🚀")

    # Obtener datos de DB
    # ...

    # Revisar datos de DB no procesados
    # ...

    # Enviar datos a API para procesar la data
    # ...

    # Obtener datos de API
    # ...