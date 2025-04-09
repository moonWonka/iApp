import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Leer variables
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = '{ODBC Driver 18 for SQL Server}'

def get_connection():
    """Función para obtener la conexión a la base de datos"""
    try:
        connection_string = f"""
            DRIVER={driver};
            SERVER={server};
            DATABASE={database};
            UID={username};
            PWD={password};
            Encrypt=yes;
            TrustServerCertificate=no;
            Connection Timeout=30;
        """
        return pyodbc.connect(connection_string)
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
        return None

def insert_log(model: str, content: str, is_processed: int=0):
    """Función para insertar logs"""
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO JOURNAL.JOURNAL_ENTRY (MODEL, CONTENT, IS_PROCESSED, EXECUTION_TIME)
            VALUES (?, ?, ?, GETDATE())
        """, (model, content, is_processed))
        conn.commit()
        print("✅ Registro insertado correctamente")
    except Exception as e:
        print("❌ Error al insertar registro:", e)
    finally:
        conn.close()

def get_logs():
    """Función para obtener logs"""
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ID, MODEL, CONTENT, IS_PROCESSED, EXECUTION_TIME
            FROM JOURNAL.JOURNAL_ENTRY
            ORDER BY EXECUTION_TIME DESC
        """)
        rows = cursor.fetchall()
        print("📝 Registros encontrados:")
        for row in rows:
            print(f"ID: {row.ID}, MODEL: {row.MODEL}, IS_PROCESSED: {row.IS_PROCESSED}, TIME: {row.EXECUTION_TIME}")
            print(f"CONTENT: {row.CONTENT}")
            print("-" * 60)
    except Exception as e:
        print("❌ Error al obtener registros:", e)
    finally:
        conn.close()
