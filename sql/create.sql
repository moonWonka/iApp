-- Eliminar tablas si ya existen
IF OBJECT_ID('PROCESO.MODEL_PROCESS_STATUS', 'U') IS NOT NULL DROP TABLE PROCESO.MODEL_PROCESS_STATUS;
IF OBJECT_ID('PROCESO.IA_RESPONSE_LOG', 'U') IS NOT NULL DROP TABLE PROCESO.IA_RESPONSE_LOG;
IF OBJECT_ID('PROCESO.PROCESSED_ARTICLES', 'U') IS NOT NULL DROP TABLE PROCESO.PROCESSED_ARTICLES;


-- Eliminar esquema si existe
IF EXISTS (SELECT * FROM sys.schemas WHERE name = 'PROCESO')
    DROP SCHEMA PROCESO;

-- Crear el esquema
CREATE SCHEMA PROCESO;

-- Tabla principal de artículos
CREATE TABLE PROCESO.PROCESSED_ARTICLES (
    ID INT IDENTITY PRIMARY KEY,               -- Identificador único del artículo

    TITULO VARCHAR(250) NOT NULL,              -- Título de la noticia
    FECHA VARCHAR(50) NOT NULL,                -- Fecha original de publicación
    URL VARCHAR(1000) NOT NULL,                -- Enlace a la fuente original
    FUENTE VARCHAR(100) NOT NULL,              -- Nombre del medio o fuente
    DESCRIPCION VARCHAR(MAX) NOT NULL          -- Resumen o contenido relevante
);

-- Tabla de logs de ejecución (todos los intentos: exitosos y fallidos)
CREATE TABLE PROCESO.IA_RESPONSE_LOG (
    ID INT IDENTITY PRIMARY KEY,               -- Identificador único del log de IA

    ARTICLE_ID INT NOT NULL,                   -- ID del artículo procesado
    MODEL_NAME VARCHAR(100) NOT NULL,          -- Nombre del modelo (ej: GPT-4, Gemini)
    PROMPT VARCHAR(MAX) NOT NULL,              -- Prompt o instrucción enviada a la IA
    RESPONSE VARCHAR(MAX) NOT NULL,            -- Respuesta completa (puede incluir errores)
    FILTERED_RESPONSE VARCHAR(MAX) NULL,       -- Respuesta útil o extraída
    STATUS_CODE INT NOT NULL,                  -- Código de estado HTTP

    RESPONSE_TIME_SEC FLOAT NULL,              -- Tiempo de respuesta en segundos
    TOKENS_USED INT NULL,                      -- Tokens consumidos
    RESPONSE_DATE DATETIME DEFAULT GETDATE(),  -- Fecha de la respuesta

    CONSTRAINT FK_Response_To_Article
        FOREIGN KEY (ARTICLE_ID)
        REFERENCES PROCESO.PROCESSED_ARTICLES(ID)
        ON DELETE CASCADE
);

-- Tabla con los resultados generados por modelo IA
CREATE TABLE PROCESO.MODEL_PROCESS_STATUS (
    ID INT IDENTITY PRIMARY KEY,                 -- Identificador único del procesamiento

    ARTICLE_ID INT NOT NULL,                     -- ID del artículo procesado
    MODEL_NAME VARCHAR(100) NOT NULL,            -- Nombre del modelo IA utilizado
    IS_PROCESSED BIT DEFAULT 0,                  -- Estado: 1 = procesado exitosamente, 0 = pendiente

    ETIQUETAS_IA VARCHAR(MAX) NULL,              -- Etiquetas generadas (temas/categorías)
    SENTIMIENTO VARCHAR(50) NULL,                -- Positivo, negativo o neutro
    RATING DECIMAL(3,1) NULL,                    -- Evaluación subjetiva (1.0 a 5.0)
    NIVEL_RIESGO VARCHAR(50) NULL,               -- Riesgo estimado: bajo, medio o alto
    INDICADOR_VIOLENCIA VARCHAR(50) NULL,        -- Sí o No
    EDAD_RECOMENDADA VARCHAR(50) NULL,           -- Edad sugerida (ej: +13, +18)
    EXECUTION_TIME VARCHAR(50) NULL,                -- Tiempo de ejecución exitoso

    CONSTRAINT FK_ModelStatus_Article FOREIGN KEY (ARTICLE_ID)
        REFERENCES PROCESO.PROCESSED_ARTICLES(ID)
        ON DELETE CASCADE
);