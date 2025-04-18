import pytz
from datetime import datetime
from models.entities import Article, IAProcessedData, Noticia, ProcessStatusDTO, IALogModel
import repository.proceso_repository as repository
from services.ia_models_service import IAService
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export import guardar_en_csv, leer_desde_csv

# Constante para la zona horaria de América/Santiago
TZ_SANTIAGO = pytz.timezone("America/Santiago")

MODELOS: list[str] = ["GEMINI", "OPENAI"]

def cargar_datos_a_db() -> None:
    """
    Carga los datos desde archivos CSV a la base de datos.
    """
    fecha_hora_actual = datetime.now(TZ_SANTIAGO)
    print(f"Fecha y hora actual en Santiago: {fecha_hora_actual}")

    diario_a: list[Noticia] = leer_desde_csv("noticias.csv")
    diario_b: list[Noticia] = leer_desde_csv("noticias2.csv")
    diarios_data: list[Noticia] = diario_a + diario_b

    print("Cargando datos desde los archivos CSV... 📂")

    for noticia in diarios_data:
        print(f"Guardado noticia: {noticia.titulo}")
        nueva_noticia = Noticia(
            titulo=noticia.titulo,
            fecha=fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
            descripcion=noticia.descripcion,
            url=noticia.url,
            fuente=noticia.fuente
        )
        articulo_id = repository.insertar_articulo(nueva_noticia)
        if articulo_id:
            for modelo in MODELOS:
                repository.insertar_status(articulo_id=articulo_id, modelo=modelo, estado_procesado=False)
    print("Inserción de datos completada con éxito 🚀")

def obtener_datos_de_db(modelo: str) -> list[Article]:
    """
    Obtiene artículos no procesados desde la base de datos para un modelo específico.

    Parámetros:
    - modelo: Nombre del modelo de IA para el cual se buscarán artículos no procesados.

    Retorna:
    - Una lista de objetos Article que no han sido procesados (IS_PROCESSED = False) para el modelo especificado.
    """
    if modelo not in MODELOS:
        print(f"⚠️ El modelo '{modelo}' no es válido. Modelos disponibles: {MODELOS}")
        return []

    try:
        articulos_modelo: list[Article] = repository.obtener_articulos_por_estado(modelo=modelo, estado_procesado=False)

        if articulos_modelo:
            print(f"✅ Modelo: {modelo} - Artículos no procesados: {len(articulos_modelo)}")
            return articulos_modelo

        print(f"⚠️ No se encontraron artículos no procesados para el modelo '{modelo}'.")
        return []

    except Exception as e:
        print(f"❌ Error al obtener datos de la base de datos para el modelo '{modelo}': {e}")
        return []


def procesar_articulo_con_ia(articulo: Article, modelo: str) -> ProcessStatusDTO:
    """
    Procesa un artículo con un modelo de IA específico.
    """
    # Crear el prompt para el modelo
    print(f"articulo a procesar: '{articulo}'")
    titulo = articulo.titulo
    descripcion = articulo.descripcion
    prompt = f"""
    Analiza el siguiente artículo de prensa y completa estrictamente los siguientes campos en formato JSON:

    Artículo:
    "{titulo}"
    "{descripcion}"

    Devuelve tu respuesta en formato JSON respetando el siguiente esquema y sin ningún comentario adicional(un json limpio):

    {{
        "etiquetas_ia": [ "etiqueta1", "etiqueta2", "..." ],
        "sentimiento": "positivo | negativo | neutro",
        "rating": "número_decimal_entre_1.0_y_5.0_nivel_de_impacto",
        "nivel_riesgo": "bajo | medio | alto",
        "indicador_violencia": "sí | no | moderado",
        "edad_recomendada": "+13 | +18 | todo público"
    }}
    """

    # Crear instancia del servicio de IA
    modeloService = IAService(prompt=prompt)

    # Diccionario para el switch
    switch_modelos = {
        "GEMINI": modeloService.call_gemini,
        "OPENAI": modeloService.call_openAI,
    }

    # Llamar al método correspondiente según el modelo
    if modelo in switch_modelos:
        data_procesada: ProcessStatusDTO = switch_modelos[modelo]()
    else:
        raise ValueError(f"Modelo '{modelo}' no soportado. Modelos disponibles: {list(switch_modelos.keys())}")

    print("🤣🤣🤣")
    print(data_procesada)

    return data_procesada

def procesar_con_modelo_ia(articulos_no_procesados: list[Article], modelo: str) -> None:
    """
    Procesa los artículos utilizando un modelo de IA, actualiza su estado en la base de datos
    y registra los resultados en la tabla de logs.
    """
    if not articulos_no_procesados:
        print("⚠️ No hay artículos para procesar.")
        return

    print(f"✅ Se encontraron {len(articulos_no_procesados)} artículos no procesados. Procesando con IA...")

    for articulo in articulos_no_procesados:
        try:
            print(articulo)
            print(f"🤖 Procesando artículo ID: {articulo.id}, Título: {articulo.titulo}...")
            resultado_ia: ProcessStatusDTO = procesar_articulo_con_ia(articulo, modelo)

            procesado_exitosamente = (
                resultado_ia.status_code == 200 and resultado_ia.is_processed
            )

            if procesado_exitosamente:
                actualizado = repository.actualizar_datos_ia(articulo.id, resultado_ia)
                mensaje = "procesado y actualizado con éxito" if actualizado else "procesado, pero no se pudo actualizar en la base de datos"
                print(f"✅ Artículo ID: {articulo.id} {mensaje}.")
            else:
                print(f"⚠️ Procesamiento fallido para el artículo ID: {articulo.id}. Código de estado: {resultado_ia.status_code}")

            log_entry = IALogModel(
                article_id=articulo.id,
                model=resultado_ia.model_used,
                prompt="PROMPT SIMULADO",  # Reemplaza por el prompt real si lo tienes
                response="RESPUESTA SIMULADA",  # Reemplaza por la respuesta real si la tienes
                filtered_response=None,
                status_code=resultado_ia.status_code,
                response_time_sec=0.5,  # simulado
                tokens_used=100,        # simulado
                log_date=datetime.now(TZ_SANTIAGO)
            )
            repository.insertar_log(log_entry)

        except Exception as e:
            print(f"❌ Error al procesar el artículo ID: {articulo.id}: {e}")
            # Registrar el error en el log
            log_entry = IALogModel(
                article_id=articulo.id,
                model=getattr(articulo, "model_name", "DESCONOCIDO"),
                prompt="PROMPT SIMULADO",
                response=f"ERROR: {str(e)}",
                filtered_response=None,
                status_code=500,
                response_time_sec=None,
                tokens_used=None,
                log_date=datetime.now(TZ_SANTIAGO)
            )
            repository.insertar_log(log_entry)
            continue

    print("🚀 Procesamiento con modelo de IA completado.")


def procesar_datos() -> None:
    """
    Función principal para procesar datos desde periódicos y realizar operaciones en la base de datos.
    """
    # Obtener información de periódicos
    #datos_diario_a: list[Noticia] = extraer_noticias_araucaniadiario(max_articulos=20)
    #datos_diario_b: list[Noticia] = extraer_noticias_elperiodico(max_articulos=20)

    # Guardar información en CSV
    #guardar_en_csv(datos_diario_a)
    #guardar_en_csv(datos_diario_b, nombre_archivo="noticias2.csv")

    # Cargar información hacia DB
    #cargar_datos_a_db()

    # Procesar datos con modelos de IA por cada modelo
    for modelo in MODELOS:
        articulos_no_procesados: list[Article] = obtener_datos_de_db(modelo)
        procesar_con_modelo_ia(articulos_no_procesados, modelo)