import pytz
from datetime import datetime
from models.entities import Article, Noticia
from repository.article_repository import insertar_articulo, obtener_articulos_por_estado
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export import guardar_en_csv, leer_desde_csv


# Constante para la zona horaria de América/Santiago
TZ_SANTIAGO = pytz.timezone("America/Santiago")

def cargar_datos_a_db() -> None:
    """
    Carga los datos desde archivos CSV a la base de datos.
    """
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
        insertar_articulo(nueva_noticia)

    print("Inserción de datos completada con éxito 🚀")

def obtener_datos_de_db() -> list[Article]:
    """
    Obtiene artículos no procesados desde la base de datos y los imprime.

    Retorna:
    - Una lista de objetos Article que no han sido procesados (IS_PROCESSED = False).
    """
    try:
        # Obtener artículos no procesados
        articulos: list[Article] = obtener_articulos_por_estado(estado_procesado=False)

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

def procesar_articulo_con_ia(articulo: Article) -> dict:
    """
    Simula el procesamiento de un artículo con un modelo de IA.

    Retorna:
    - Un diccionario con los resultados del modelo de IA.
    """
    # Simulación de resultados del modelo de IA
    return {
        "etiquetas_ia": "noticia, política",
        "sentimiento": "positivo",
        "rating": 4.5,
        "nivel_riesgo": "bajo",
        "indicador_violencia": False,
        "edad_recomendada": 18,
        "model_used": "ModeloIA_v1",
        "execution_time": "2025-04-14 10:00:00",
        "is_processed": True
    }

def actualizar_articulo_en_db(articulo_id: int, datos_actualizados: dict) -> None:
    """
    Actualiza un artículo en la base de datos con los datos proporcionados.

    Parámetros:
    - articulo_id: ID del artículo a actualizar.
    - datos_actualizados: Diccionario con los datos actualizados.
    """

    # Aquí se implementaría la lógica para actualizar el artículo en la base de datos.
    print(f"🔄 Actualizando artículo ID: {articulo_id} en la base de datos con los datos: {datos_actualizados}")

def procesar_con_modelo_ia(articulos_no_procesados: list[Article]) -> None:
    """
    Procesa los artículos utilizando un modelo de IA y actualiza su estado en la base de datos.

    Parámetros:
    - articulos_no_procesados: Lista de objetos Article que no han sido procesados.
    """
    if not articulos_no_procesados:
        print("⚠️ No hay artículos no procesados para procesar.")
        return

    print(f"✅ Se encontraron {len(articulos_no_procesados)} artículos no procesados. Procesando con IA...")

    for articulo in articulos_no_procesados:
        try:
            # Simular el procesamiento con un modelo de IA
            print(f"🤖 Procesando artículo ID: {articulo.id}, Título: {articulo.titulo}...")
            resultado_ia = procesar_articulo_con_ia(articulo)  # Llamada al modelo de IA

            # Actualizar el artículo con los resultados del modelo de IA
            actualizar_articulo_en_db(articulo.id, resultado_ia)
            print(f"✅ Artículo ID: {articulo.id} procesado con éxito.")

        except Exception as e:
            print(f"❌ Error al procesar el artículo ID: {articulo.id}: {e}")
            continue  # Continuar con el siguiente artículo si ocurre un error

    print("🚀 Procesamiento con modelo de IA completado.")





def procesar_datos() -> None:
    """
    Función principal para procesar datos desde periódicos y realizar operaciones en la base de datos.
    """
    # # Obtener información de periódicos
    # datos_diario_a: list[Noticia] = extraer_noticias_araucaniadiario(max_articulos=100)
    # datos_diario_b: list[Noticia] = extraer_noticias_elperiodico(max_articulos=100)

    # # Guardar información en CSV
    # guardar_en_csv(datos_diario_a)
    # guardar_en_csv(datos_diario_b, nombre_archivo="noticias2.csv")

    # # Cargar información hacia DB
    # cargar_datos_a_db()

    # Obtener datos de DB
    articulos_no_procesados: list[Article] = obtener_datos_de_db()

    # Procesar datos con modelos de IA
    procesar_con_modelo_ia(articulos_no_procesados)