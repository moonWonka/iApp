from dataclasses import dataclass
from datetime import datetime

@dataclass
class Noticia:
    titulo: str            # Título de la noticia
    fecha: str             # Fecha en que fue publicada
    url: str               # URL desde donde se extrajo
    fuente: str            # Fuente de la noticia ("Araucanía Diario")
    descripcion: str       # Breve resumen o contenido inicial de la noticia

@dataclass
class Article:
    id: int                                     # Identificador único del artículo
    titulo: str                                 # Título de la noticia
    fecha: str                                  # Fecha original de publicación
    url: str                                    # Enlace a la fuente original
    fuente: str                                 # Nombre del medio o fuente
    descripcion: str                            # Resumen o contenido relevante

    etiquetas_ia: str | None = None             # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str | None = None              # Sentimiento: positivo, negativo o neutro
    rating: float | None = None                 # Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str | None = None             # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str | None = None      # Indicación si contiene violencia
    edad_recomendada: str | None = None         # Edad sugerida de lectura (+13, +18)
    execution_time: str | None = None           # Fecha y hora del análisis (formato string)
    is_processed: bool | None = None            # Indica si el artículo fue procesado por el modelo
    model_name: str | None = None               # Nombre del modelo IA utilizado

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
    log_date: datetime | None = None            # Fecha y hora del log

@dataclass
class RespuestaIA:
    etiquetas_ia: str
    sentimiento: str
    rating: float
    nivel_riesgo: str
    indicador_violencia: str  # <-- Cambiado a str para reflejar la DB
    edad_recomendada: str     # <-- Cambiado a str para reflejar la DB
    model_used: str
    execution_time: str
    status_code: int
    is_processed: bool

@dataclass
class ProcessStatusDTO:
    etiquetas_ia: str                # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str                 # Sentimiento detectado (positivo, negativo o neutro)
    rating: float                    # Calificación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str                # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str         # Indicación si contiene violencia
    status_code: int                 # Código HTTP
    edad_recomendada: str            # Edad sugerida de lectura (+13, +18, etc.)
    execution_time: str              # Fecha y hora del análisis (formato string)
    model_used: str                  # Nombre del modelo de IA utilizado
    is_processed: bool
