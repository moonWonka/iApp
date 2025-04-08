import requests
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()
#Token
OPENAI_API_KEY = ""
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def call_openAI():
    """Realizar petición Modelo OPENAPI gpt-4o"""
    url: str = "https://api.openai.com/v1/responses"
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"  
    }
    payload: dict[str, str] = {
        "model": "gpt-4o",
        "input": "Write a one-sentence bedtime story about a unicorn."
    }

    response = requests.post(url, headers=headers, json=payload)

    # Verificar si la petición fue exitosa 
    if response.status_code == 200:
        print("Respuesta exitosa:")
        print(response.json())  # Imprimir el contenido en formato JSON
    else:
        print(f"Error en la petición: {response.status_code}")
        try:
            # Intentar imprimir el contenido de la respuesta en formato JSON
            error_response = response.json() 
            print("Respuesta del servicio:", error_response)
        except ValueError:
            # Si no se puede decodificar como JSON, mostrar el texto de la respuesta
            print("No se pudo decodificar la respuesta como JSON. Respuesta en texto:")
            print(response.text)


def call_gemini():
      # type: ignore
    url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers: dict[str, str] = {
        "Content-Type": "application/json"
    }

    queryparam: dict[str, str | None] = {
        "key": GEMINI_API_KEY
    }

    data = {
        "contents": [ 
            {
                "parts": [
                    {
                        "text": "responde siempre en español,  como dices me divierte mucho hablar de esto wonka en portuges"
                    }
                ]
            } 
        ]
    }

    response = requests.post(url, json=data, headers=headers, params=queryparam)
    # Obtener el tiempo de respuesta
    response_time = response.elapsed.total_seconds()
    print(f"Tiempo de respuesta: {response_time:.2f} segundos")    
    return response.json()



modeloGemini = call_gemini()

print(modeloGemini)
