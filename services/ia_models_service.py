import requests
import os
from config.settings import GEMINI_API_KEY, OPENAI_API_KEY 

class IAService:

    def __init__(self, prompt: str):
        self.prompt = prompt

    def call_openAI(self, prompt: str):   
        """Realizar petición Modelo OPENAPI gpt-4o"""
        url: str = "https://api.openai.com/v1/responses"
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"  
        }
        payload: dict[str, str] = {
            "model": "gpt-4o",
            "input": self.prompt
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


    def call_gemini(self, prompt: str):
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
                            "text": self.prompt
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
