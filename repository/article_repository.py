from models.entities import Article
from repository.connection import get_connection

def insert_article(title: str, date: str, url: str, source: str, description: str, is_processed: int = 0) -> int | None:
    """
    Inserta un artículo en la tabla PROCESO.PROCESSED_ARTICLES.

    Parámetros:
    - title: Título de la noticia o artículo.
    - date: Fecha asociada al artículo.
    - url: Enlace directo al artículo original.
    - source: Fuente de la información (ej. 'El Periódico').
    - description: Extracto o contenido preliminar del artículo.
    - is_processed: Indica si el artículo ya fue procesado por IA (0 o 1, por defecto 0).

    Retorna:
    - El ID generado del artículo insertado (int) o None si falló.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO PROCESO.PROCESSED_ARTICLES (
                TITULO, FECHA, URL, FUENTE, DESCRIPCION, IS_PROCESSED
            )
            OUTPUT INSERTED.ID
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (title, date, url, source, description, is_processed))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return inserted_id
    except Exception as e:
        print("❌ Error al insertar artículo:", e)
        return None
    finally:
        conn.close()

def get_articles_by_processed_status(processed_status: int) -> list[Article]:
    """
    Obtiene artículos filtrados por el campo IS_PROCESSED.

    Parámetros:
    - processed_status: 0 para no procesados, 1 para procesados.

    Retorna:
    - Una lista de objetos Article con los artículos encontrados.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                ID, TITULO, FECHA, URL, FUENTE, DESCRIPCION,
                ETIQUETAS_IA, SENTIMIENTO, RATING, NIVEL_RIESGO,
                INDICADOR_VIOLENCIA, EDAD_RECOMENDADA,
                MODEL_USED, EXECUTION_TIME, IS_PROCESSED
            FROM PROCESO.PROCESSED_ARTICLES
            WHERE IS_PROCESSED = ?
        """
        cursor.execute(query, (processed_status,))
        rows = cursor.fetchall()

        return [
            Article(
                id=row.ID,
                titulo=row.TITULO,
                fecha=row.FECHA,
                url=row.URL,
                fuente=row.FUENTE,
                descripcion=row.DESCRIPCION,
                etiquetas_ia=row.ETIQUETAS_IA,
                sentimiento=row.SENTIMIENTO,
                rating=row.RATING,
                nivel_riesgo=row.NIVEL_RIESGO,
                indicador_violencia=row.INDICADOR_VIOLENCIA,
                edad_recomendada=row.EDAD_RECOMENDADA,
                model_used=row.MODEL_USED,
                execution_time=row.EXECUTION_TIME,
                is_processed=row.IS_PROCESSED,
            )
            for row in rows
        ]
    except Exception as e:
        print("❌ Error al obtener artículos:", e)
        return []
    finally:
        conn.close()
