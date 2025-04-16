from models.entities import Article, Noticia
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
                is_processed=bool(fila.IS_PROCESSED)
            )
            for fila in filas
        ]
    except Exception as e:
        print("❌ Error al obtener artículos:", e)
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

def actualizar_datos_ia(articulo_id: int, datos_ia: dict) -> bool:
    """
    Actualiza los datos generados por la IA en la tabla MODEL_PROCESS_STATUS.

    Parámetros:
    - articulo_id (int): ID del artículo.
    - datos_ia (dict): Diccionario con los siguientes campos:
        - etiquetas_ia (str): Etiquetas generadas por IA.
        - sentimiento (str): Sentimiento detectado.
        - rating (float): Calificación subjetiva.
        - nivel_riesgo (str): Nivel de riesgo.
        - indicador_violencia (str): Indicador de violencia.
        - edad_recomendada (str): Edad recomendada.
        - execution_time (str): Fecha/hora de ejecución.
        - model_used (str): Nombre del modelo de IA.

    Retorna:
    - bool: True si la actualización fue exitosa, False si hubo error.
    """
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(queries.UPDATE_ARTICULO_IA, (
            datos_ia["etiquetas_ia"],
            datos_ia["sentimiento"],
            datos_ia["rating"],
            datos_ia["nivel_riesgo"],
            datos_ia["indicador_violencia"],
            datos_ia["edad_recomendada"],
            datos_ia["execution_time"],
            articulo_id,
            datos_ia["model_used"]
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Error al actualizar los datos del artículo ID {articulo_id}:", e)
        return False
    finally:
        conn.close()
