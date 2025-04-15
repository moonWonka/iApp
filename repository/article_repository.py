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
        query = """
            INSERT INTO PROCESO.PROCESSED_ARTICLES (
                TITULO, FECHA, URL, FUENTE, DESCRIPCION
            )
            OUTPUT INSERTED.ID
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
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

def obtener_articulos_por_estado(estado_procesado: bool, modelo: str) -> list[Article]:
    """
    Obtiene artículos filtrados por el campo IS_PROCESSED y el modelo de IA.
    Si un artículo no tiene un registro en ARTICLE_MODEL_STATUS, también será incluido.

    Parámetros:
    - estado_procesado: False para no procesados, True para procesados.
    - modelo: Nombre del modelo de IA utilizado.

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
                pa.ID, 
                pa.TITULO, 
                pa.FECHA, 
                pa.URL, 
                pa.FUENTE, 
                pa.DESCRIPCION,
                pa.ETIQUETAS_IA, 
                pa.SENTIMIENTO, 
                pa.RATING, 
                pa.NIVEL_RIESGO,
                pa.INDICADOR_VIOLENCIA, 
                pa.EDAD_RECOMENDADA, 
                pa.EXECUTION_TIME,
                COALESCE(ams.IS_PROCESSED, 0) AS IS_PROCESSED  -- Si no hay registro, asumir no procesado
            FROM PROCESO.PROCESSED_ARTICLES pa
            LEFT JOIN PROCESO.ARTICLE_MODEL_STATUS ams
                ON pa.ID = ams.ARTICLE_ID AND ams.MODEL = ?
            WHERE COALESCE(ams.IS_PROCESSED, 0) = ?
        """
        # Convertir el booleano a entero para la consulta SQL (False -> 0, True -> 1)
        cursor.execute(query, (modelo, int(estado_procesado)))
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
                is_processed=bool(fila.IS_PROCESSED)  # Convertir a booleano
            )
            for fila in filas
        ]
    except Exception as e:
        print("❌ Error al obtener artículos:", e)
        return []
    finally:
        conn.close()

def actualizar_datos_ia(articulo_id: int, datos_ia: dict) -> bool:
    """
    Actualiza los datos generados por la IA en la tabla PROCESSED_ARTICLES.

    Parámetros:
    - articulo_id: ID del artículo a actualizar.
    - datos_ia: Diccionario con los datos generados por la IA.

    Retorna:
    - True si la actualización fue exitosa, False en caso contrario.
    """
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            UPDATE PROCESO.PROCESSED_ARTICLES
            SET 
                ETIQUETAS_IA = ?, 
                SENTIMIENTO = ?, 
                RATING = ?, 
                NIVEL_RIESGO = ?, 
                INDICADOR_VIOLENCIA = ?, 
                EDAD_RECOMENDADA = ?, 
                EXECUTION_TIME = ?
            WHERE ID = ?
        """
        cursor.execute(query, (
            datos_ia["etiquetas_ia"],
            datos_ia["sentimiento"],
            datos_ia["rating"],
            datos_ia["nivel_riesgo"],
            datos_ia["indicador_violencia"],
            datos_ia["edad_recomendada"],
            datos_ia["execution_time"],
            articulo_id
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar los datos del artículo ID {articulo_id}:", e)
        return False
    finally:
        conn.close()

def verificar_status_existente(articulo_id: int, modelo: str) -> bool:
    """
    Verifica si ya existe un registro en ARTICLE_MODEL_STATUS para un artículo y modelo.

    Parámetros:
    - articulo_id: ID del artículo.
    - modelo: Nombre del modelo de IA.

    Retorna:
    - True si el registro existe, False en caso contrario.
    """
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*)
            FROM PROCESO.ARTICLE_MODEL_STATUS
            WHERE ARTICLE_ID = ? AND MODEL = ?
        """
        cursor.execute(query, (articulo_id, modelo))
        existe = cursor.fetchone()[0] > 0
        return existe
    except Exception as e:
        print(f"❌ Error al verificar el estado del artículo ID {articulo_id} y modelo {modelo}:", e)
        return False
    finally:
        conn.close()

def insertar_status(articulo_id: int, modelo: str, estado_procesado: bool) -> bool:
    """
    Inserta un nuevo estado en ARTICLE_MODEL_STATUS.

    Parámetros:
    - articulo_id: ID del artículo.
    - modelo: Nombre del modelo de IA.
    - estado_procesado: Estado del proceso (True para procesado, False para no procesado).

    Retorna:
    - True si la inserción fue exitosa, False en caso contrario.
    """
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO PROCESO.ARTICLE_MODEL_STATUS (ARTICLE_ID, MODEL, IS_PROCESSED)
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (articulo_id, modelo, int(estado_procesado)))
        conn.commit()
        print(f"✅ Nuevo estado insertado para el artículo ID {articulo_id} y modelo {modelo}.")
        return True
    except Exception as e:
        print(f"❌ Error al insertar el estado del artículo ID {articulo_id} y modelo {modelo}:", e)
        return False
    finally:
        conn.close()

def actualizar_status(articulo_id: int, modelo: str, estado_procesado: bool) -> bool:
    """
    Actualiza el estado existente en ARTICLE_MODEL_STATUS.

    Parámetros:
    - articulo_id: ID del artículo.
    - modelo: Nombre del modelo de IA.
    - estado_procesado: Estado del proceso (True para procesado, False para no procesado).

    Retorna:
    - True si la actualización fue exitosa, False en caso contrario.
    """
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
            UPDATE PROCESO.ARTICLE_MODEL_STATUS
            SET IS_PROCESSED = ?
            WHERE ARTICLE_ID = ? AND MODEL = ?
        """
        cursor.execute(query, (int(estado_procesado), articulo_id, modelo))
        conn.commit()
        print(f"🔄 Estado actualizado para el artículo ID {articulo_id} y modelo {modelo}.")
        return True
    except Exception as e:
        print(f"❌ Error al actualizar el estado del artículo ID {articulo_id} y modelo {modelo}:", e)
        return False
    finally:
        conn.close()
