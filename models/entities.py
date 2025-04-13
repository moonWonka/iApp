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
    id: int | None = None                     # Identificador único del artículo
    titulo: str                               # Título de la noticia
    fecha: str                                # Fecha original de publicación
    url: str                                  # Enlace a la fuente original
    fuente: str                               # Nombre del medio o fuente
    descripcion: str                          # Resumen o contenido relevante

    etiquetas_ia: str | None = None           # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str | None = None            # Sentimiento: positivo, negativo o neutro
    rating: float | None = None               # Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str | None = None           # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str | None = None    # Indicación si contiene violencia
    edad_recomendada: str | None = None       # Edad sugerida de lectura (+13, +18, etc.)

    model_used: str | None = None             # Modelo IA utilizado para el análisis
    execution_time: str | None = None         # Fecha y hora del análisis (formato datetime como string)

    is_processed: bool = False                # Indica si el artículo ya fue procesado (False = no, True = sí) 

@dataclass
class IAResponseLog:
    id: int | None = None                       # Identificador único del log
    article_id: int                             # ID del artículo asociado (FK obligatoria)
    model: str                                  # Modelo IA utilizado
    status_code: int                            # Código de estado HTTP de la respuesta
    response_text: str                          # Texto completo de la respuesta (incluye errores si los hay)
    response: str | None = None                 # Respuesta útil filtrada (sin errores ni metadatos)
    execution_time: float | None = None         # Tiempo que demoró la IA en generar la respuesta (en segundos)
    tokens_used: int | None = None              # Cantidad de tokens utilizados en la generación
    log_date: str | None = None                 # Fecha y hora en que se registró esta entrada (formato datetime como string)