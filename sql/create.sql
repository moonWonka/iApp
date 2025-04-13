-- Eliminar tablas si existen
IF OBJECT_ID('PROCESO.IA_RESPONSE_LOG', 'U') IS NOT NULL
    DROP TABLE PROCESO.IA_RESPONSE_LOG;

IF OBJECT_ID('PROCESO.PROCESSED_ARTICLES', 'U') IS NOT NULL
    DROP TABLE PROCESO.PROCESSED_ARTICLES;

-- Eliminar esquema si existe
IF EXISTS (SELECT * FROM sys.schemas WHERE name = 'PROCESO')
    DROP SCHEMA PROCESO;

-- Crear esquema
CREATE SCHEMA PROCESO;

-- Crear tabla PROCESSED_ARTICLES
CREATE TABLE PROCESO.PROCESSED_ARTICLES (
    ID INT IDENTITY PRIMARY KEY,               -- Identificador único del artículo

    TITULO VARCHAR(250) NOT NULL,              -- Título de la noticia
    FECHA VARCHAR(50) NOT NULL,                -- Fecha original de publicación
    URL VARCHAR(1000) NOT NULL,                -- Enlace a la fuente original
    FUENTE VARCHAR(100) NOT NULL,              -- Nombre del medio o fuente
    DESCRIPCION VARCHAR(MAX) NOT NULL,         -- Resumen o contenido relevante

    ETIQUETAS_IA VARCHAR(MAX) NULL,            -- Etiquetas generadas por IA (temas o categorías)
    SENTIMIENTO VARCHAR(50) NULL,              -- Sentimiento: positivo, negativo o neutro
    RATING DECIMAL(3,1) NULL,                  -- Evaluación subjetiva del artículo (escala 1.0 a 5.0)
    NIVEL_RIESGO VARCHAR(50) NULL,             -- Nivel de riesgo estimado: bajo, medio o alto
    INDICADOR_VIOLENCIA VARCHAR(50) NULL,      -- Indicación si contiene violencia
    EDAD_RECOMENDADA VARCHAR(50) NULL,         -- Edad sugerida de lectura (+13, +18, etc.)

    MODEL_USED VARCHAR(100) NULL,              -- Modelo IA utilizado para el análisis
    EXECUTION_TIME DATETIME NULL,              -- Fecha y hora del análisis

    IS_PROCESSED BIT DEFAULT 0                 -- Indica si el artículo ya fue procesado (0 = no, 1 = sí)
);

-- Crear tabla IA_RESPONSE_LOG
CREATE TABLE PROCESO.IA_RESPONSE_LOG (
    ID INT IDENTITY PRIMARY KEY,               -- Identificador único de la respuesta IA

    ARTICLE_ID INT NOT NULL,                   -- Referencia al artículo procesado
    MODEL_NAME VARCHAR(100) NOT NULL,          -- Nombre del modelo de IA utilizado
    PROMPT VARCHAR(MAX) NOT NULL,              -- Prompt o instrucción enviada a la IA
    RESPONSE VARCHAR(MAX) NOT NULL,            -- Respuesta completa (JSON, errores, etc.)
    FILTERED_RESPONSE VARCHAR(MAX) NULL,       -- Contenido útil extraído de la respuesta
    STATUS_CODE INT NOT NULL,                  -- Código de estado (ej: 200, 500, etc.)

    RESPONSE_TIME_SEC FLOAT NULL,              -- Tiempo de respuesta en segundos
    TOKENS_USED INT NULL,                      -- Cantidad de tokens utilizados en la llamada
    RESPONSE_DATE DATETIME DEFAULT GETDATE(),  -- Fecha y hora en que se recibió la respuesta

    CONSTRAINT FK_Response_To_Article
        FOREIGN KEY (ARTICLE_ID)
        REFERENCES PROCESO.PROCESSED_ARTICLES(ID)
        ON DELETE CASCADE
);











