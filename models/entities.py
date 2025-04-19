from dataclasses import dataclass
from datetime import datetime

@dataclass
class Noticia:
    """
    Representa una noticia extraída de una fuente específica.
    """
    titulo: str            # Título de la noticia
    fecha: str             # Fecha en que fue publicada
    url: str               # URL desde donde se extrajo
    fuente: str            # Fuente de la noticia (por ejemplo, "Araucanía Diario")
    descripcion: str       # Breve resumen o contenido inicial de la noticia


@dataclass
class Article:
    """
    Representa un artículo procesado o no procesado por IA.
    """
    id: int                                     # Identificador único del artículo
    titulo: str                                 # Título de la noticia
    fecha: str                                  # Fecha original de publicación
    url: str                                    # Enlace a la fuente original
    fuente: str                                 # Nombre del medio o fuente
    descripcion: str                            # Resumen o contenido relevante

    etiquetas_ia: str | None = None             # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str | None = None              # Sentimiento detectado: positivo, negativo o neutro
    rating: float | None = None                 # Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str | None = None             # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str | None = None      # Indicación si contiene violencia
    edad_recomendada: str | None = None         # Edad sugerida de lectura (+13, +18)
    execution_time: str | None = None           # Tiempo de procesamiento del artículo (formato string)
    is_processed: bool | None = None            # Indica si el artículo fue procesado por el modelo
    model_name: str | None = None               # Nombre del modelo IA utilizado


@dataclass
class IALogModel:
    """
    Representa un registro de log generado durante el procesamiento de un artículo por IA.
    """
    article_id: int                             # ID del artículo procesado
    status_code: int                            # Código de estado HTTP del procesamiento
    model: str                                  # Nombre del modelo IA utilizado
    prompt: str                                 # Prompt enviado al modelo IA
    response: str                               # Respuesta completa del modelo IA
    filtered_response: str | None = None       # Respuesta filtrada o procesada
    response_time_sec: float | None = None     # Tiempo de respuesta del modelo IA en segundos
    tokens_used: int | None = None             # Número de tokens utilizados en la respuesta
    log_date: datetime | None = None           # Fecha y hora del registro


@dataclass
class RespuestaIA:
    """
    Representa la respuesta generada por IA para un artículo.
    """
    etiquetas_ia: str                           # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str                            # Sentimiento detectado: positivo, negativo o neutro
    rating: float                               # Calificación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str                           # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str                    # Indicación si contiene violencia
    edad_recomendada: str                       # Edad sugerida de lectura (+13, +18)
    model_used: str                             # Nombre del modelo IA utilizado
    execution_time: str                         # Tiempo de procesamiento del artículo (formato string)
    status_code: int                            # Código de estado HTTP del procesamiento
    is_processed: bool                          # Indica si el artículo fue procesado con éxito


@dataclass
class ProcessStatusDTO:
    """
    DTO para representar el estado del procesamiento de un artículo por IA.
    """
    etiquetas_ia: str                           # Etiquetas generadas por IA (temas o categorías)
    sentimiento: str                            # Sentimiento detectado: positivo, negativo o neutro
    rating: float                               # Calificación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str                           # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str                    # Indicación si contiene violencia
    status_code: int                            # Código de estado HTTP del procesamiento
    edad_recomendada: str                       # Edad sugerida de lectura (+13, +18)
    execution_time: str                         # Tiempo de procesamiento del artículo (formato string)
    model_used: str                             # Nombre del modelo IA utilizado
    is_processed: bool                          # Indica si el artículo fue procesado con éxito


@dataclass
class IAProcessedData:
    """
    Representa los datos procesados por IA para un artículo.
    """
    etiquetas_ia: list[str]                     # Lista de etiquetas generadas por IA
    sentimiento: str                            # Sentimiento detectado: positivo, negativo o neutro
    rating: float                               # Calificación subjetiva del artículo (escala 1.0 a 5.0)
    nivel_riesgo: str                           # Nivel de riesgo estimado: bajo, medio o alto
    indicador_violencia: str                    # Indicación si contiene violencia
    edad_recomendada: str                       # Edad sugerida de lectura (+13, +18)


@dataclass
class AnalisisResumenDTO:
    """
    DTO para representar el análisis de resumen generado por IA.

    Relacionado con:
    - PROMPT_RESUMEN_EJECUTIVO: Genera un resumen ejecutivo basado en métricas como distribución de sentimientos,
      artículos por fuente, niveles de riesgo y promedio de rating por fuente.
    """
    titulo: str                                 # Título del resumen
    resumen: str                                # Resumen generado por IA
    elementos_clave: list[dict]                # Elementos clave identificados en el análisis
    posibles_implicaciones: list[str]          # Implicaciones sociales o mediáticas
    preguntas_pendientes: list[str]            # Preguntas clave generadas por IA


@dataclass
class RiesgoEvaluacionDTO:
    """
    DTO para representar la evaluación de riesgo realizada por IA.

    Relacionado con:
    - PROMPT_EVALUACION_RIESGOS_SOCIALES: Evalúa el impacto social de los sentimientos negativos,
      niveles de riesgo alto e indicadores de violencia detectados en las noticias.
    """
    riesgo_general: str                         # Evaluación general del riesgo
    factores_detonantes: list[str]             # Factores que contribuyen al riesgo
    recomendaciones: list[str]                 # Recomendaciones para mitigar el riesgo


@dataclass
class EvaluacionImpactoDTO:
    """
    DTO para representar la evaluación de impacto por IA.

    Relacionado con:
    - PROMPT_EVALUACION_RIESGOS_SOCIALES: Genera hipótesis sobre las consecuencias sociales a corto o mediano plazo
      basadas en tendencias de riesgo y violencia detectadas en las noticias.
    """
    impacto_social: str                         # Descripción del impacto social
    grupos_afectados: list[str]                # Grupos sociales afectados por el impacto
    urgencia_respuesta: str                    # Nivel de urgencia para responder al impacto


@dataclass
class PropuestaAccionDTO:
    """
    DTO para representar propuestas de acción sugeridas por IA.

    Relacionado con:
    - PROMPT_EVALUACION_RIESGOS_SOCIALES: Proporciona recomendaciones para mitigar riesgos sociales
      detectados en las noticias.
    """
    acciones_recomendadas: list[str]           # Lista de acciones sugeridas
    actores_clave: list[str]                   # Actores clave involucrados en las acciones
    tiempo_estimado: str                       # Tiempo estimado para implementar las acciones


@dataclass
class PreguntasCriticasDTO:
    """
    DTO para representar preguntas clave generadas por IA para profundizar el análisis.

    Relacionado con:
    - PROMPT_RESUMEN_EJECUTIVO: Genera preguntas pendientes o críticas basadas en el análisis de métricas
      como distribución de sentimientos, niveles de riesgo y rating por fuente.
    """
    preguntas_clave: list[str]                 # Lista de preguntas clave generadas por IA


@dataclass
class TendenciasSentimientoDTO:
    """
    DTO para representar el análisis de tendencias emocionales generado por IA.

    Relacionado con:
    - PROMPT_TENDENCIAS_SENTIMIENTO: Analiza la tendencia emocional predominante en un conjunto de noticias,
      considerando sentimientos, niveles de riesgo, violencia y rating promedio.
    """
    titulo: str                                 # Título del análisis de tendencias
    resumen: str                                # Resumen generado por IA
    elementos_clave: list[str]                 # Elementos clave identificados en el análisis
    posibles_implicaciones: list[str]          # Implicaciones sociales o mediáticas
    preguntas_pendientes: list[str]            # Preguntas clave generadas por IA