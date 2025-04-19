import pytz
import pandas as pd
from datetime import datetime
from models.entities import AnalisisResumenDTO, Article, IAProcessedData, Noticia, ProcessStatusDTO, IALogModel
import repository.proceso_repository as repository
from services.ia_models_service import IAService
from services.scraping.scraping import extraer_noticias_elperiodico, extraer_noticias_araucaniadiario
from services.file_export.csv_writer import guardar_articles_en_csv, guardar_noticias_en_csv
from services.file_export import leer_desde_csv
from core.prompts_analysis import PROMPT_ANALISIS_ARTICULO, PROMPT_COMPARATIVO_MEDIOS, PROMPT_RESUMEN_EJECUTIVO

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


def obtener_datos_de_db(modelo: str, estado_procesado: bool) -> list[Article]:
    """
    Obtiene artículos desde la base de datos para un modelo específico y un estado de procesamiento.

    Parámetros:
    - modelo: Nombre del modelo de IA para el cual se buscarán artículos.
    - estado_procesado: True para buscar artículos procesados, False para buscar artículos no procesados.

    Retorna:
    - Una lista de objetos Article que cumplen con el estado de procesamiento especificado para el modelo.
    """
    if modelo not in MODELOS:
        print(f"⚠️ El modelo '{modelo}' no es válido. Modelos disponibles: {MODELOS}")
        return []

    try:
        articulos_modelo: list[Article] = repository.obtener_articulos_por_estado(modelo=modelo, estado_procesado=estado_procesado)

        if articulos_modelo:
            estado_texto = "procesados" if estado_procesado else "no procesados"
            print(f"✅ Modelo: {modelo} - Artículos {estado_texto}: {len(articulos_modelo)}")
            return articulos_modelo

        estado_texto = "procesados" if estado_procesado else "no procesados"
        print(f"⚠️ No se encontraron artículos {estado_texto} para el modelo '{modelo}'.")
        return []

    except Exception as e:
        print(f"❌ Error al obtener datos de la base de datos para el modelo '{modelo}': {e}")
        return []


def procesar_articulo_con_ia(articulo: Article, modelo: str) -> ProcessStatusDTO:
    """
    Procesa un artículo con un modelo de IA específico.
    """
    # Crear el prompt para el modelo utilizando el prompt centralizado
    print(f"articulo a procesar: '{articulo}'")
    titulo = articulo.titulo
    descripcion = articulo.descripcion
    prompt = PROMPT_ANALISIS_ARTICULO.format(titulo=titulo, descripcion=descripcion)

    # Crear instancia del servicio de IA
    modeloService = IAService(prompt=prompt)

    # Diccionario para el switch
    switch_modelos = {
        "GEMINI": modeloService.call_gemini,
        "OPENAI": modeloService.call_openAI,  # Método específico para ProcessStatusDTO
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


def guardar_articulos_procesados_en_csv() -> None:
    """
    Obtiene los artículos procesados para ambos modelos y los guarda en un archivo CSV.
    """
    print("🔄 Obteniendo artículos procesados para ambos modelos...")
    articulos_procesados: list[Article] = []
    for modelo in MODELOS:
        articulos_procesados.extend(obtener_datos_de_db(modelo=modelo, estado_procesado=True))

    # Escribir los datos procesados en un archivo CSV
    if articulos_procesados:
        print("✍️ Escribiendo artículos procesados en un archivo CSV...")
        guardar_articles_en_csv(articulos_procesados, nombre_archivo="articulos_procesados.csv")
        print("✅ Artículos procesados guardados en 'articulos_procesados.csv'.")
    else:
        print("⚠️ No se encontraron artículos procesados para guardar en el archivo CSV.")


def analizar_métricas_desde_csv(nombre_archivo: str = "articulos_procesados.csv") -> None:
    """
    Carga los artículos procesados desde un archivo CSV y genera métricas de análisis.
    """
    try:
        df = pd.read_csv(nombre_archivo)

        print("\n📊 Métricas Generales del CSV:")
        print(f"Total de artículos: {len(df)}")
        print("\n📰 Artículos por fuente:")
        print(df['fuente'].value_counts())

        print("\n😊 Distribución de Sentimientos:")
        print(df['sentimiento'].value_counts())

        print("\n⭐ Promedio de Rating por Fuente:")
        print(df.groupby('fuente')['rating'].mean())

        print("\n🔥 Nivel de Riesgo por frecuencia:")
        print(df['nivel_riesgo'].value_counts())

    except Exception as e:
        print(f"❌ Error al analizar métricas desde el CSV: {e}")


def generar_resumen_ejecutivo(modelo: str) -> None:
    """
    Genera un resumen ejecutivo basado en los datos procesados y utiliza un modelo de IA para analizarlo.

    Parámetros:
    - modelo: Nombre del modelo de IA a utilizar ("OPENAI" o "GEMINI").
    """
    try:
        # Leer los datos procesados desde el archivo CSV
        nombre_archivo = "articulos_procesados.csv"
        df = pd.read_csv(nombre_archivo)

        # Preparar los datos para el prompt
        distribucion_fuente = df['fuente'].value_counts().to_dict()
        distribucion_sentimiento = df['sentimiento'].value_counts().to_dict()
        rating_por_fuente = df.groupby('fuente')['rating'].mean().to_dict()
        niveles_riesgo = df['nivel_riesgo'].value_counts().to_dict()

        # Crear el prompt para el resumen ejecutivo
        prompt = PROMPT_RESUMEN_EJECUTIVO.format(
            distribucion_fuente=distribucion_fuente,
            distribucion_sentimiento=distribucion_sentimiento,
            rating_por_fuente=rating_por_fuente,
            niveles_riesgo=niveles_riesgo
        )

        print(prompt)

        # Crear instancia del servicio de IA
        modeloService = IAService(prompt=prompt)

        # Llamar al modelo para generar el resumen ejecutivo
        if modelo == "OPENAI":
            resumen: AnalisisResumenDTO = modeloService.call_openAI(prompt_type="resumen_ejecutivo")
        elif modelo == "GEMINI":
            resumen: AnalisisResumenDTO = modeloService.call_gemini(prompt_type="resumen_ejecutivo")
        else:
            raise ValueError(f"Modelo '{modelo}' no soportado. Modelos disponibles: {MODELOS}")

        # Mostrar el resumen generado
        print("\n📋 Resumen Ejecutivo Generado:")
        print(f"Título: {resumen.titulo}")
        print(f"Resumen: {resumen.resumen}")
        print(f"Elementos Clave: {resumen.elementos_clave}")
        print(f"Posibles Implicaciones: {resumen.posibles_implicaciones}")
        print(f"Preguntas Pendientes: {resumen.preguntas_pendientes}")

    except Exception as e:
        print(f"❌ Error al generar el resumen ejecutivo: {e}")


def procesar_datos() -> None:
    """
    Función principal para procesar datos desde periódicos y realizar operaciones en la base de datos.
    """
    # Obtener información de periódicos
    # datos_diario_a: list[Noticia] = extraer_noticias_araucaniadiario(max_articulos=50)
    # datos_diario_b: list[Noticia] = extraer_noticias_elperiodico(max_articulos=50)

    # Guardar información en CSV
    # guardar_noticias_en_csv(datos_diario_a)
    # guardar_noticias_en_csv(datos_diario_b, nombre_archivo="noticias2.csv")

    # Cargar información hacia DB
    # cargar_datos_a_db()

    # Procesar datos con modelos de IA por cada modelo
    # for modelo in MODELOS:
    #     articulos_no_procesados: list[Article] = obtener_datos_de_db(modelo, False)
    #     procesar_con_modelo_ia(articulos_no_procesados, modelo)

    # Llamar al método independiente para guardar los artículos procesados en un CSV
    # guardar_articulos_procesados_en_csv()
    analizar_métricas_desde_csv()
    for modelo in MODELOS:
        generar_resumen_ejecutivo(modelo=modelo)

