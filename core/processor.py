import pytz
from datetime import datetime
import time
from models.entities import Article, Noticia, RespuestaIA, IALogModel
from repository.article_repository import actualizar_datos_ia, insertar_articulo, obtener_articulos_por_estado, insertar_status, actualizar_status
from repository.log_respository import insertar_log
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export import guardar_en_csv, leer_desde_csv


# Constante para la zona horaria de América/Santiago
TZ_SANTIAGO = pytz.timezone("America/Santiago")

MODELOS:list[str] = ["GEMINI", "OPENAI"]

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
        print(f"Guardado noticia: {noticia.titulo}")

        # Crear el objeto Noticia
        nueva_noticia = Noticia(
            titulo=noticia.titulo,
            fecha=fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            descripcion=noticia.descripcion,
            url=noticia.url,
            fuente=noticia.fuente
        )

        # Insertar la noticia en la base de datos
        articulo_id = insertar_articulo(nueva_noticia)

        if articulo_id:
            # Insertar el estado inicial para los modelos GEMINI y OPENAI
            for modelo in MODELOS:
                insertar_status(articulo_id=articulo_id, modelo=modelo, estado_procesado=False)

    print("Inserción de datos completada con éxito 🚀")

def obtener_datos_de_db(modelo: str) -> list[Article]:
    """
    Obtiene artículos no procesados desde la base de datos para un modelo específico.

    Parámetros:
    - modelo: Nombre del modelo de IA para el cual se buscarán artículos no procesados.

    Retorna:
    - Una lista de objetos Article que no han sido procesados (IS_PROCESSED = False) para el modelo especificado.
    """
    try:
        if modelo not in MODELOS:
            print(f"⚠️ El modelo '{modelo}' no es válido. Modelos disponibles: {MODELOS}")
            return []

        # Obtener artículos no procesados para el modelo especificado
        articulos_modelo: list[Article] = obtener_articulos_por_estado(modelo=modelo, estado_procesado=False)

        if not articulos_modelo:
            print(f"⚠️ No se encontraron artículos no procesados para el modelo '{modelo}'.")
            return []

        print(f"✅ Modelo: {modelo} - Artículos no procesados: {len(articulos_modelo)}")
        for articulo in articulos_modelo:
            print(f"  - ID: {articulo.id}, Título: {articulo.titulo}")

        return articulos_modelo

    except Exception as e:
        print(f"❌ Error al obtener datos de la base de datos para el modelo '{modelo}': {e}")
        return []

def procesar_articulo_con_ia(articulo: Article) -> RespuestaIA:
    """
    Simula el procesamiento de un artículo con un modelo de IA.

    Parámetros:
    - articulo: Objeto Article que representa el artículo a procesar.

    Retorna:
    - Una instancia de RespuestaIA con los resultados del modelo de IA.
    """
    # Simular un delay
    time.sleep(0.5)

    # Simulación de resultados del modelo de IA
    return RespuestaIA(
        etiquetas_ia="noticia, política",
        sentimiento="positivo",
        rating=4.5,
        nivel_riesgo="bajo",
        indicador_violencia=False,
        edad_recomendada=18,
        model_used="GEMINI",
        execution_time="2025-04-14 10:00:00",
        status_code=200,
        is_processed=True
    )

def procesar_con_modelo_ia(articulos_no_procesados: list[Article]) -> None:
    """
    Procesa los artículos utilizando un modelo de IA, actualiza su estado en la base de datos
    y registra los resultados en la tabla de logs.

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
            resultado_ia: RespuestaIA = procesar_articulo_con_ia(articulo)  # Llamada al modelo de IA

            # Actualizar el artículo con los resultados del modelo de IA
            if resultado_ia.status_code == 200 and resultado_ia.is_processed:
                actualizar_datos_ia(articulo.id, resultado_ia.__dict__)  # Convertir RespuestaIA a dict
                actualizar_status(articulo.id, resultado_ia.model_used, estado_procesado=True)
                print(f"✅ Artículo ID: {articulo.id} procesado con éxito.")
            else:
                print(f"⚠️ Procesamiento fallido para el artículo ID: {articulo.id}. Código de estado: {resultado_ia.status_code}")

            # Registrar en la tabla de logs
            log_entry = IALogModel(
                article_id=articulo.id,
                model=resultado_ia.model_used,
                status_code=resultado_ia.status_code,
                response_text="Procesado correctamente" if resultado_ia.is_processed else "Error en el procesamiento",
                response=None,
                execution_time=0.5,  # Simulación del tiempo de procesamiento
                tokens_used=100,  # Simulación de tokens utilizados
                log_date=datetime.now(TZ_SANTIAGO).strftime("%Y-%m-%d %H:%M:%S")
            )
            insertar_log(log_entry)

        except Exception as e:
            print(f"❌ Error al procesar el artículo ID: {articulo.id}: {e}")

            # Registrar el error en la tabla de logs
            log_entry = IALogModel(
                article_id=articulo.id,
                model="Desconocido",
                status_code=500,
                response_text=f"Error: {str(e)}",
                response=None,
                execution_time=None,
                tokens_used=None,
                log_date=datetime.now(TZ_SANTIAGO).strftime("%Y-%m-%d %H:%M:%S")
            )
            insertar_log(log_entry)
            continue  # Continuar con el siguiente artículo si ocurre un error

    print("🚀 Procesamiento con modelo de IA completado.")

def procesar_datos() -> None:
    """
    Función principal para procesar datos desde periódicos y realizar operaciones en la base de datos.
    """
    # Obtener información de periódicos
    datos_diario_a: list[Noticia] = extraer_noticias_araucaniadiario(max_articulos=100)
    datos_diario_b: list[Noticia] = extraer_noticias_elperiodico(max_articulos=100)

    # Guardar información en CSV
    guardar_en_csv(datos_diario_a)
    guardar_en_csv(datos_diario_b, nombre_archivo="noticias2.csv")

    # Cargar información hacia DB
    cargar_datos_a_db()

    # Obtener datos de DB
    articulos_no_procesados: list[Article] = obtener_datos_de_db()

    # Procesar datos con modelos de IA
    procesar_con_modelo_ia(articulos_no_procesados)