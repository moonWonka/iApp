# ----------- ANALÍTICA CON IA (TEXT PROMPTS) -----------

# Opción 1: Análisis de Tendencias
PROMPT_TENDENCIAS_SENTIMIENTO = """
Analiza el siguiente conjunto de datos agregados de noticias:
- Sentimientos detectados por IA (frecuencia):
  positivo: {positivo}, negativo: {negativo}, neutro: {neutro}, neutral: {neutral}

Con base en estos datos, describe cuál es la tendencia emocional predominante en las noticias.
Incluye interpretación social o mediática que podría estar reflejando.
"""

# Opción 2: Resumen Ejecutivo Automático
PROMPT_RESUMEN_EJECUTIVO = """
Con base en las siguientes métricas extraídas de un conjunto de noticias analizadas por IA:
- Artículos por fuente:
{distribucion_fuente}
- Distribución de sentimientos:
{distribucion_sentimiento}
- Promedio de rating por fuente:
{rating_por_fuente}
- Niveles de riesgo identificados:
{niveles_riesgo}

Genera un resumen ejecutivo de estilo profesional que describa el comportamiento editorial observado.
Devuelve tu respuesta en formato JSON respetando el siguiente esquema y sin ningún comentario adicional (un JSON limpio):

{{
    "titulo": "Título del resumen ejecutivo",
    "resumen": "Texto del resumen ejecutivo",
    "elementos_clave": [ "elemento1", "elemento2", "..." ],
    "posibles_implicaciones": [ "implicacion1", "implicacion2", "..." ],
    "preguntas_pendientes": [ "pregunta1", "pregunta2", "..." ]
}}
"""

# Opción 3: Recomendación para Audiencia
PROMPT_RECOMENDACION_AUDIENCIA = """
Estas noticias han sido etiquetadas con niveles de edad recomendada y temas potencialmente sensibles:

- Edad recomendada más frecuente: {edad_mas_frecuente}
- Niveles de riesgo: {resumen_niveles_riesgo}
- Presencia de violencia: {conteo_violencia}

Recomienda para qué tipo de audiencia deberían estar destinadas estas noticias.
Incluye un comentario sobre cómo afecta esto a lectores jóvenes o vulnerables.
"""

# Opción 4: Evaluación de Riesgos Sociales
PROMPT_EVALUACION_RIESGOS_SOCIALES = """
Con base en los siguientes datos agregados de un sistema de análisis de noticias:
- Sentimientos negativos: {negativos}
- Nivel de riesgo alto: {riesgo_alto}
- Indicadores de violencia detectados: {indicador_violencia}

Evalúa qué tipo de impacto social podría tener este tipo de contenido en los lectores.
Genera una hipótesis sobre consecuencias a corto o mediano plazo si esta tendencia se mantiene.
"""

# Opción 5: Reporte comparativo entre medios
PROMPT_COMPARATIVO_MEDIOS = """
Comparación entre los siguientes medios según su análisis por IA:

Araucanía Diario:
- Rating promedio: {rating_araucania}
- Sentimiento predominante: {sentimiento_araucania}
- Nivel de riesgo más frecuente: {riesgo_araucania}

El Periódico:
- Rating promedio: {rating_periodico}
- Sentimiento predominante: {sentimiento_periodico}
- Nivel de riesgo más frecuente: {riesgo_periodico}

Redacta un reporte comparativo sobre estilo editorial, tono y grado de riesgo en la información de cada fuente.
"""

# Opción 6: Análisis de Artículo Individual
PROMPT_ANALISIS_ARTICULO = """
Analiza el siguiente artículo de prensa y completa estrictamente los siguientes campos en formato JSON:

Artículo:
"{titulo}"
"{descripcion}"

Devuelve tu respuesta en formato JSON respetando el siguiente esquema y sin ningún comentario adicional(un json limpio):

{{
    "etiquetas_ia": [ "etiqueta1", "etiqueta2", "..." ],
    "sentimiento": "positivo | negativo | neutro",
    "rating": "número_decimal_entre_1.0_y_5.0_nivel_de_impacto",
    "nivel_riesgo": "bajo | medio | alto",
    "indicador_violencia": "sí | no | moderado",
    "edad_recomendada": "+13 | +18 | todo público"
}}
"""
