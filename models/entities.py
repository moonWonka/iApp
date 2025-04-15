from dataclasses import dataclass

@dataclass
class Noticia:
    titulo: str            # Título de la noticia
    fecha: str             # Fecha en que fue publicada
    url: str               # URL desde donde se extrajo
    fuente: str            # Fuente de la noticia (ej. "Araucanía Diario")
    descripcion: str       # Breve resumen o contenido inicial de la noticia

@dataclass
class Article:
    titulo: str                                 # Título de la noticia
    fecha: str                                  # Fecha original de publicación
    url: str                                    # Enlace a la fuente original
    fuente: str                                 # Nombre del medio o fuente
    descripcion: str                            # Resumen o contenido relevante

    id: int | None = None                       # Identificador único del artículo
    etiquetas_ia: str | None = None             # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str | None = None              # Sentimiento: positivo, negativo o neutro
    rating: float | None = None                 # Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str | None = None             # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str | None = None      # Indicación si contiene violencia
    edad_recomendada: str | None = None         # Edad sugerida de lectura (+13, +18, etc.)
    model_used: str | None = None               # Modelo IA utilizado para el análisis
    execution_time: str | None = None           # Fecha y hora del análisis (formato string)

@dataclass
class IALogModel:
    article_id: int                             # ID del artículo asociado (FK obligatoria)
    model: str                                  # Modelo IA utilizado
    status_code: int                            # Código HTTP
    response_text: str                          # Texto completo de la respuesta (con errores si los hay)

    id: int | None = None                       # Identificador único del log
    response: str | None = None                 # Respuesta útil filtrada
    execution_time: float | None = None         # Tiempo de respuesta en segundos
    tokens_used: int | None = None              # Tokens utilizados
    log_date: str | None = None                 # Fecha y hora del log (formato string)

@dataclass
class RespuestaIA:
    """
    Clase que modela la respuesta generada por el servicio de modelos de IA.
    """
    etiquetas_ia: str                          # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str                           # Sentimiento: positivo, negativo o neutro
    rating: float                              # Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str                          # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: bool                  # Indicación si contiene violencia
    edad_recomendada: int                      # Edad sugerida de lectura (+13, +18, etc.)
    model_used: str                            # Modelo IA utilizado para el análisis
    execution_time: str                        # Fecha y hora del análisis (formato string)
    status_code: int                           # Código HTTP para indicar el estado del procesamiento (200 = OK)
    is_processed: bool                         # Indica si el artículo fue procesado correctamente
