from repository.connection import get_connection

def insert_article(
    title: str,
    date: str,
    url: str,
    source: str,
    description: str,
    is_processed: int = 0
) -> int | None:
    """
    Inserta un artículo en la tabla PROCESSED.ARTICLES.

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
            INSERT INTO PROCESSED.ARTICLES (
                TITLE,
                DATE,
                URL,
                SOURCE,
                DESCRIPTION,
                IS_PROCESSED
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (title, date, url, source, description, is_processed))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("❌ Error al insertar artículo:", e)
        return None
    finally:
        conn.close()
