from models.entities import Article, Noticia
from repository.connection import get_connection

def insertar_articulo(noticia: Noticia) -> int | None:
    """
    Inserta un artículo en la tabla PROCESO.PROCESSED_ARTICLES.

    Parámetros:
    - noticia: Objeto Noticia que contiene los datos del artículo.

    Retorna:
    - El ID generado del artículo insertado (int) o None si falló.
    """
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        consulta = """
            INSERT INTO PROCESO.PROCESSED_ARTICLES (
                TITULO, FECHA, URL, FUENTE, DESCRIPCION
            )
            OUTPUT INSERTED.ID
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(consulta, (
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

def obtener_articulos_por_estado(estado_procesado: bool) -> list[Article]:
    """
    Obtiene artículos filtrados por el campo IS_PROCESSED.

    Parámetros:
    - estado_procesado: False para no procesados, True para procesados.

    Retorna:
    - Una lista de objetos Article con los artículos encontrados.
    """
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        consulta = """
            SELECT 
                ID, TITULO, FECHA, URL, FUENTE, DESCRIPCION,
                ETIQUETAS_IA, SENTIMIENTO, RATING, NIVEL_RIESGO,
                INDICADOR_VIOLENCIA, EDAD_RECOMENDADA,
                MODEL_USED, EXECUTION_TIME, IS_PROCESSED
            FROM PROCESO.PROCESSED_ARTICLES
            WHERE IS_PROCESSED = ?
        """
        # Convertir el booleano a entero para la consulta SQL (False -> 0, True -> 1)
        cursor.execute(consulta, (int(estado_procesado),))
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
                model_used=fila.MODEL_USED,
                execution_time=fila.EXECUTION_TIME,
                is_processed=bool(fila.IS_PROCESSED),  # Convertir a booleano
            )
            for fila in filas
        ]
    except Exception as e:
        print("❌ Error al obtener artículos:", e)
        return []
    finally:
        conn.close()
