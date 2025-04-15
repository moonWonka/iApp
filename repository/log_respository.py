from repository.connection import get_connection

def insertar_log(
    article_id: int,
    model: str,
    status_code: int,
    response_text: str,
    execution_time: float | None = None,
    tokens_used: int | None = None,
    log_date: str | None = None
) -> int | None:
    """
    Inserta un registro en la tabla de logs IA_RESPONSE_LOG.

    Parámetros:
    - article_id: ID del artículo asociado al log.
    - model: Nombre del modelo de IA utilizado.
    - status_code: Código de estado del procesamiento (ej. 200 para éxito, 500 para error).
    - response_text: Mensaje o texto de respuesta del procesamiento.
    - execution_time: Tiempo de ejecución del procesamiento (en segundos).
    - tokens_used: Número de tokens utilizados durante el procesamiento.
    - log_date: Fecha y hora del log (formato string, opcional).

    Retorna:
    - El ID generado del registro insertado (int) o None si falló.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO IA_RESPONSE_LOG (
                ARTICLE_ID,
                MODEL,
                STATUS_CODE,
                RESPONSE_TEXT,
                EXECUTION_TIME,
                TOKENS_USED,
                LOG_DATE
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (article_id, model, status_code, response_text, execution_time, tokens_used, log_date))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("❌ Error al insertar log:", e)
        return None
    finally:
        conn.close()
