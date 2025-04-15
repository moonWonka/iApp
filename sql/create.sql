-- Eliminar tablas si existen (en orden por dependencias)
IF OBJECT_ID('PROCESO.ARTICLE_MODEL_STATUS', 'U') IS NOT NULL DROP TABLE PROCESO.ARTICLE_MODEL_STATUS;
IF OBJECT_ID('PROCESO.IA_RESPONSE_LOG', 'U') IS NOT NULL DROP TABLE PROCESO.IA_RESPONSE_LOG;
IF OBJECT_ID('PROCESO.PROCESSED_ARTICLES', 'U') IS NOT NULL DROP TABLE PROCESO.PROCESSED_ARTICLES;

-- Eliminar esquema si existe
IF EXISTS (SELECT * FROM sys.schemas WHERE name = 'PROCESO')
    DROP SCHEMA PROCESO;

-- Crear el esquema
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

    EXECUTION_TIME DATETIME NULL,              -- Fecha y hora del análisis
);

-- Crear tabla IA_RESPONSE_LOG
CREATE TABLE PROCESO.IA_RESPONSE_LOG (
    ID INT IDENTITY PRIMARY KEY,               -- Identificador único del log de IA

    ARTICLE_ID INT NOT NULL,                   -- ID del artículo procesado
    MODEL_NAME VARCHAR(100) NOT NULL,          -- Nombre del modelo (ej: GPT-4, Gemini)
    PROMPT VARCHAR(MAX) NOT NULL,              -- Prompt o instrucción enviada a la IA
    RESPONSE VARCHAR(MAX) NOT NULL,            -- Respuesta completa (puede incluir errores)
    FILTERED_RESPONSE VARCHAR(MAX) NULL,       -- Respuesta filtrada o útil
    STATUS_CODE INT NOT NULL,                  -- Código de estado HTTP u otro código relevante

    RESPONSE_TIME_SEC FLOAT NULL,              -- Tiempo de respuesta en segundos
    TOKENS_USED INT NULL,                      -- Tokens consumidos
    RESPONSE_DATE DATETIME DEFAULT GETDATE(),  -- Fecha en que se registró la respuesta

    CONSTRAINT FK_Response_To_Article
        FOREIGN KEY (ARTICLE_ID)
        REFERENCES PROCESO.PROCESSED_ARTICLES(ID)
        ON DELETE CASCADE
);


-- Crear tabla de control por modelo
CREATE TABLE PROCESO.ARTICLE_MODEL_STATUS (
    ID INT IDENTITY PRIMARY KEY,               -- ID único del registro
    ARTICLE_ID INT NOT NULL,                   -- ID del artículo
    MODEL VARCHAR(100) NOT NULL,               -- Nombre del modelo
    IS_PROCESSED BIT DEFAULT 0,                -- 0 = pendiente, 1 = procesado

    CONSTRAINT FK_ModelStatus_Article
        FOREIGN KEY (ARTICLE_ID)
        REFERENCES PROCESO.PROCESSED_ARTICLES(ID)
        ON DELETE CASCADE
);
