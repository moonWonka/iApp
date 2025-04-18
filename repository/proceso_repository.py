from models.entities import Article, Noticia, ProcessStatusDTO, IALogModel
from repository.connection import get_connection
from . import queries

# ----------- QUERYS (SELECT) -----------

def obtener_articulos_por_estado(estado_procesado: bool, modelo: str) -> list[Article]:
    """
    Obtiene artículos filtrados por el campo IS_PROCESSED y el modelo de IA.
    Si un artículo no tiene un registro en MODEL_PROCESS_STATUS, también será incluido.

    Parámetros:
    - estado_procesado (bool): True para artículos procesados, False para no procesados.
    - modelo (str): Nombre del modelo de IA ("GEMINI", "OPENAI").

    Retorna:
    - list[Article]: Lista de objetos Article con los datos del artículo y su estado de procesamiento.
    """
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_ARTICULOS_POR_ESTADO, (modelo, int(estado_procesado)))
        filas = cursor.fetchall()
        return [
            Article(
                id=fila.ID,
                titulo=fila.TITULO,
                fecha=fila.FECHA,
                url=fila.URL,
                fuente=fila.FUENTE,
                descripcion=fila.DESCRIPCION,
                etiquetas_ia=fila.ETIQUETAS_IA,
                sentimiento=fila.SENTIMIENTO,
                rating=fila.RATING,
                nivel_riesgo=fila.NIVEL_RIESGO,
                indicador_violencia=fila.INDICADOR_VIOLENCIA,
                edad_recomendada=fila.EDAD_RECOMENDADA,
                execution_time=fila.EXECUTION_TIME,
                is_processed=bool(fila.IS_PROCESSED),
                model_name=fila.MODEL_NAME
            )
            for fila in filas
        ]
    except Exception as e:
        print("❌ Error al obtener artículos🚀🚀:", e)
        return []
    finally:
        conn.close()

def verificar_status_existente(articulo_id: int, modelo: str) -> bool:
    """
    Verifica si ya existe un registro en MODEL_PROCESS_STATUS para un artículo y modelo.

    Parámetros:
    - articulo_id (int): ID del artículo.
    - modelo (str): Nombre del modelo de IA.

    Retorna:
    - bool: True si existe el registro, False si no existe o hay error.
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(queries.EXISTE_STATUS, (articulo_id, modelo))
        existe = cursor.fetchone()[0] > 0
        return existe
    except Exception as e:
        print(f"❌ Error al verificar el estado del artículo ID {articulo_id} y modelo {modelo}:", e)
        return False
    finally:
        conn.close()

# ----------- COMMANDS (INSERT/UPDATE) -----------

def insertar_articulo(noticia: Noticia) -> int | None:
    """
    Inserta un artículo en la tabla PROCESSED_ARTICLES.

    Parámetros:
    - noticia (Noticia): Objeto con los campos:
        - titulo (str): Título del artículo.
        - fecha (str): Fecha del artículo.
        - url (str): URL de la noticia.
        - fuente (str): Fuente o medio.
        - descripcion (str): Contenido o resumen.

    Retorna:
    - int | None: ID del artículo insertado o None si falla.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(queries.INSERT_ARTICULO, (
            noticia.titulo,
            noticia.fecha,
            noticia.url,
            noticia.fuente,
            noticia.descripcion
        ))
        id_insertado = cursor.fetchone()[0]
        conn.commit()
        return id_insertado
    except Exception as e:
        print("❌ Error al insertar artículo:", e)
        return None
    finally:
        conn.close()

def insertar_status(articulo_id: int, modelo: str, estado_procesado: bool) -> bool:
    """
    Inserta un nuevo estado en MODEL_PROCESS_STATUS.

    Parámetros:
    - articulo_id (int): ID del artículo.
    - modelo (str): Nombre del modelo de IA.
    - estado_procesado (bool): True si ya fue procesado, False si no.

    Retorna:
    - bool: True si la inserción fue exitosa, False si hubo error.
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(queries.INSERTAR_STATUS, (articulo_id, modelo, int(estado_procesado)))
        conn.commit()
        print(f"✅ Nuevo estado insertado para el artículo ID {articulo_id} y modelo {modelo}.")
        return True
    except Exception as e:
        print(f"❌ Error al insertar el estado del artículo ID {articulo_id} y modelo {modelo}:", e)
        return False
    finally:
        conn.close()

def insertar_log(
    article_id: int,
    model_name: str,
    prompt: str,
    response: str,
    status_code: int,
    filtered_response: str | None = None,
    response_time_sec: float | None = None,
    tokens_used: int | None = None,
    response_date: str | None = None
) -> int | None:
    """
    Inserta un registro en la tabla de logs IA_RESPONSE_LOG.

    Parámetros:
    - article_id: ID del artículo asociado al log.
    - model_name: Nombre del modelo de IA utilizado.
    - prompt: Prompt enviado al modelo.
    - response: Respuesta completa del modelo.
    - filtered_response: Respuesta filtrada (opcional).
    - status_code: Código de estado del procesamiento (ej. 200 para éxito, 500 para error).
    - response_time_sec: Tiempo de respuesta en segundos (opcional).
    - tokens_used: Número de tokens utilizados durante el procesamiento (opcional).
    - response_date: Fecha y hora del log (formato string, opcional).

    Retorna:
    - El ID generado del registro insertado (int) o None si falló.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(queries.INSERT_LOG, (
            article_id,
            model_name,
            prompt,
            response,
            filtered_response,
            status_code,
            response_time_sec,
            tokens_used,
            response_date
        ))
        id_insertado = cursor.fetchone()[0]
        conn.commit()
        return id_insertado
    except Exception as e:
        print("❌ Error al insertar log:", e)
        return None
    finally:
        conn.close()

def insertar_log(log: IALogModel) -> int | None:
    """
    Inserta un registro en la tabla de logs IA_RESPONSE_LOG usando un objeto IALogModel.

    Parámetros:
    - log (IALogModel): Objeto con los datos del log.

    Retorna:
    - El ID generado del registro insertado (int) o None si falló.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(queries.INSERT_LOG, (
            log.article_id,
            log.model,
            log.prompt,
            log.response,
            log.filtered_response,
            log.status_code,
            log.response_time_sec,
            log.tokens_used,
            log.log_date.strftime("%Y-%m-%d %H:%M:%S") if log.log_date else None
        ))
        id_insertado = cursor.fetchone()[0]
        conn.commit()
        return id_insertado
    except Exception as e:
        print("❌ Error al insertar log:", e)
        return None
    finally:
        conn.close()

def actualizar_datos_ia(articulo_id: int, datos_ia: ProcessStatusDTO) -> bool:
    """
    Actualiza los datos generados por la IA en la tabla MODEL_PROCESS_STATUS.
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()

        # Convertir lista de etiquetas a string
        etiquetas_str = ", ".join(datos_ia.etiquetas_ia) if isinstance(datos_ia.etiquetas_ia, list) else datos_ia.etiquetas_ia

        cursor.execute(queries.UPDATE_ARTICULO_IA, (
            etiquetas_str,
            datos_ia.sentimiento,
            datos_ia.rating,
            datos_ia.nivel_riesgo,
            datos_ia.indicador_violencia,
            datos_ia.edad_recomendada,
            datos_ia.execution_time,
            articulo_id,
            datos_ia.model_used
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar los datos del artículo ID {articulo_id}:", e)
        return False
    finally:
        conn.close()

