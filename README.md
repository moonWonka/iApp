# 🧠 Eva IA

Eva IA es una aplicación modular en Python que permite:

-   Realizar scraping de noticias desde múltiples fuentes, como **Araucanía Diario** y **El Periódico**.
-   Almacenar artículos en una base de datos relacional.
-   Procesar artículos utilizando modelos de lenguaje como **OpenAI** y **Gemini**.
-   Generar análisis de tendencias emocionales y métricas basadas en los datos procesados.
-   Enriquecer artículos con etiquetas, sentimiento, rating, nivel de riesgo, y más.
-   Exportar datos procesados a archivos CSV para análisis posterior.
-   Generar resúmenes ejecutivos y análisis de tendencias emocionales utilizando IA.
-   Registrar las respuestas de IA y trazabilidad mediante logs.

---

## 🚀 Requisitos

Antes de ejecutar el proyecto, tener instalado:

### 🐍 Dependencias

-   Python 3.8 o superior
-   `requests`
-   `python-dotenv`
-   `pyodbc`
-   `bs4`
-   `pytz`
-   `pandas`
-   `jupyter`
-   `matplotlib`
-   `seaborn`

Instalar todo desde:

```bash
pip install -r requirements.txt
```

---

## 📂 Funcionalidades principales

### 1. Scraping de noticias

Eva IA extrae noticias de fuentes como **Araucanía Diario** y **El Periódico**, y las guarda en archivos CSV.

### 2. Procesamiento con modelos de IA

Los artículos se procesan utilizando modelos de lenguaje como **OpenAI** y **Gemini**, generando análisis detallados y enriqueciendo los datos con información adicional.

### 3. Análisis y métricas

-   Generación de métricas como distribución de sentimientos, nivel de riesgo, y rating promedio por fuente.
-   Análisis de tendencias emocionales y resúmenes ejecutivos basados en los datos procesados.

### 4. Exportación de datos

Los datos procesados se exportan a archivos CSV para facilitar su análisis y visualización.

### 5. Registro y trazabilidad

Se registran las respuestas de los modelos de IA, incluyendo prompts, respuestas, tiempos de procesamiento, y más, para garantizar la trazabilidad.

---

## ⚙️ Ejecución

1. Ejecutar la aplicación principal:

    ```bash
    python main.py
    ```

2. Procesar datos:
   La aplicación extraerá noticias, procesará los datos con modelos de IA, generará métricas y guardará los resultados en archivos CSV automáticamente.

3. Analizar resultados:
   Los resultados procesados estarán disponibles en archivos CSV para su análisis posterior.

---

## 📊 Análisis de datos

Eva IA permite analizar los datos procesados para obtener información como:

-   Distribución de artículos por fuente.
-   Distribución de sentimientos (positivo, negativo, neutro).
-   Nivel de riesgo (bajo, medio, alto).
-   Rating promedio por fuente.
-   Tendencias emocionales y resúmenes ejecutivos generados por IA.

---
